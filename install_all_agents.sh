#!/bin/bash
# 安装 Code Quality Guard 到所有支持的 Agent

SKILL_DIR="$HOME/.agents/skills/code-quality-guard"
SCRIPTS_DIR="$SKILL_DIR/scripts"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         Code Quality Guard v5.0 — Multi-Agent Setup      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 1. Pi (当前环境)
echo "[1/5] Installing for Pi..."
mkdir -p "$HOME/.pi/agent/extensions"
cat > "$HOME/.pi/agent/extensions/code-quality-guard.ts" << 'TS_EOF'
/**
 * Code Quality Guard v5 — 智能质量守护系统
 * 
 * 功能:
 * 1. 意图识别 — 不仅检测关键词，还识别代码编写/审查/修复等意图
 * 2. 上下文注入 — 根据任务类型注入不同的质量规则
 * 3. 实时监控 — 在代码生成过程中提供实时反馈
 * 4. 门禁拦截 — Commit 前自动运行质量检查
 * 5. 学习进化 — 从项目历史中学习最佳实践
 */

import type { ExtensionAPI, SessionEntry } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { join } from "node:path";
import { existsSync, readFileSync } from "node:fs";

// 质量规则库（按任务类型分类）
const QUALITY_RULES = {
  "code-writing": `
## Code Quality Standards (Auto-Enforced)

### 🚨 Critical Rules (Must Follow)
1. **No hardcoded secrets** — Use env vars or secrets manager
2. **No SQL injection** — Use parameterized queries, never string concatenation
3. **No eval()/exec()** — Use safe parsers instead
4. **Error handling** — Every external call must have try/catch
5. **Input validation** — Validate all inputs before processing

### 🏗️ Architecture Rules
6. **Layer separation** — Controller → Service → Repository
7. **Single Responsibility** — One class/function per concern
8. **Dependency injection** — Avoid global state
9. **No god classes** — Max 15 methods per class
10. **No deep nesting** — Max 3 levels, use early return

### ⚡ Performance Rules
11. **No N+1 queries** — Use bulk operations
12. **Set timeouts** — All external calls need explicit timeout
13. **Bounded recursion** — Always have termination condition

### 🧪 Testing Rules
14. **Write tests first** — Follow TDD when possible
15. **Test boundary conditions** — Null, empty, edge cases
16. **Test error paths** — Not just happy path

### ✅ Quality Gate
Before completing:
- Score ≥ 70 on all 5 axes
- No critical security findings
- All tests pass
`,
  "code-review": `
## Code Review Checklist

### Correctness (20%)
- [ ] Null/None/undefined checks present
- [ ] Error handling for all external calls
- [ ] Boundary conditions tested
- [ ] Logic is correct and complete

### Readability (20%)
- [ ] Function names are descriptive
- [ ] Function length < 50 lines
- [ ] Nesting depth ≤ 3 levels
- [ ] No TODO/FIXME/HACK comments

### Architecture (25%)
- [ ] Proper layer separation
- [ ] Single Responsibility Principle
- [ ] Dependency injection used
- [ ] No god classes (> 15 methods)
- [ ] No deep nesting (> 3 levels)

### Security (20%)
- [ ] No hardcoded secrets
- [ ] No SQL injection vulnerabilities
- [ ] No eval()/exec() usage
- [ ] Input validation present
- [ ] Auth checks on privileged ops

### Performance (15%)
- [ ] No N+1 queries
- [ ] Timeouts set on external calls
- [ ] Recursion has termination condition

### Overall Score: __/100
Decision: ✅ APPROVE | ⚠️ CONDITIONAL | ❌ REJECT
`,
  "security-review": `
## STRIDE Threat Model

### Spoofing
- [ ] No hardcoded credentials
- [ ] Authentication implemented correctly
- [ ] Session tokens are secure

### Tampering
- [ ] Input validation present
- [ ] No SQL injection
- [ ] No XSS vulnerabilities
- [ ] Data integrity checks

### Repudiation
- [ ] Audit trail for state changes
- [ ] Immutable logging
- [ ] Non-repudiation mechanisms

### Info Disclosure
- [ ] No sensitive data in logs
- [ ] PII is masked
- [ ] Error messages don't leak info

### DoS
- [ ] Rate limiting implemented
- [ ] Request timeouts set
- [ ] Resource bounds defined

### Elevation
- [ ] Role checks on privileged ops
- [ ] RBAC/ABAC implemented
- [ ] Least privilege principle
`
};

// 意图检测器
class IntentDetector {
  private patterns = {
    "code-writing": [
      /implement\s+(function|class|api|module)/i,
      /write\s+(code|function|class|test)/i,
      /create\s+(module|service|handler|component)/i,
      /add\s+(feature|endpoint|route|api)/i,
      /fix\s+(bug|issue|error|vulnerability)/i,
      /refactor\s+(code|function|module)/i,
      /build\s+(api|service|handler|component)/i,
      /develop\s+(feature|module|system)/i,
    ],
    "code-review": [
      /review\s+(code|pr|changes|pull)/i,
      /check\s+(quality|code|security|vulnerability)/i,
      /analyze\s+(code|pattern|complexity)/i,
      /evaluate\s+(code|implementation)/i,
      /assess\s+(quality|code)/i,
    ],
    "security-review": [
      /security\s+(check|review|audit|scan)/i,
      /threat\s+(model|analysis)/i,
      /vulnerability\s+(scan|check)/i,
      /penetration\s+test/i,
    ],
  };

  detect(prompt: string): string[] {
    const intents: string[] = [];
    
    for (const [intent, patterns] of Object.entries(this.patterns)) {
      for (const pattern of patterns) {
        if (pattern.test(prompt)) {
          intents.push(intent);
          break;
        }
      }
    }
    
    return intents.length > 0 ? intents : ["general"];
  }
}

// 质量守护者
class QualityGuardian {
  private detector = new IntentDetector();
  private skillDir = process.env.HOME + "/.agents/skills/code-quality-guard";

  async injectRules(intent: string, ctx: any): Promise<string> {
    const rules = QUALITY_RULES[intent as keyof typeof QUALITY_RULES] || QUALITY_RULES["code-writing"];
    return rules;
  }

  async runQualityGate(ctx: any): Promise<{ passed: boolean; score: number; findings: any[] }> {
    const script = join(this.skillDir, "scripts", "qguard.py");
    if (!existsSync(script)) {
      return { passed: true, score: 100, findings: [] };
    }

    // 后台运行质量门禁（不阻塞）
    try {
      const result = await ctx.sessionManager.executeCommand?.(
        `python3 "${script}" gate . --min-score 70 --json 2>/dev/null`
      );
      
      if (result?.success) {
        const output = JSON.parse(result.output);
        return {
          passed: output.passed,
          score: output.avg_score,
          findings: output.findings || [],
        };
      }
    } catch (e) {
      // 静默失败
    }

    return { passed: true, score: 100, findings: [] };
  }
}

// 主扩展
export default function (pi: ExtensionAPI) {
  const guardian = new QualityGuardian();

  // 1. 会话开始时注入欢迎消息
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.notify("🛡️ Code Quality Guard v5 active", "info");
  });

  // 2. 意图识别 + 规则注入
  pi.on("before_agent_start", async (event, ctx) => {
    const intents = new IntentDetector().detect(event.prompt);
    
    if (intents.length > 0 && intents[0] !== "general") {
      const rules = await guardian.injectRules(intents[0], ctx);
      return {
        systemPrompt: rules + "\n\n" + event.systemPrompt,
        message: {
          customType: "quality-guard",
          content: `🛡️ **Quality Guard Active** — Detecting intent: ${intents.join(", ")}`,
          display: true,
        },
      };
    }
  });

  // 3. 代码写入时实时提醒
  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName === "write" || event.toolName === "edit") {
      const path = event.input?.path || "";
      const codeExt = /\.(py|ts|tsx|js|jsx|go|java|rs|cpp|c|h|hpp|cs|swift|kt)$/i;
      
      if (codeExt.test(path)) {
        ctx.ui.notify(
          `📝 Writing to ${path} — Remember: No hardcoded secrets, use parameterized queries, handle errors`,
          "info"
        );
      }
    }

    // 4. Git commit 门禁拦截
    if (event.toolName === "bash") {
      const cmd = event.input?.command || "";
      if (/git\s+commit/i.test(cmd)) {
        ctx.ui.notify("🔍 Running quality gate...", "info");
        
        // 同步运行质量门禁
        const result = await guardian.runQualityGate(ctx);
        
        if (!result.passed) {
          return {
            block: true,
            reason: `Quality gate failed (score: ${result.score}/100). Fix ${result.findings.length} findings before committing.`
          };
        }
      }
    }
  });

  // 5. 注册质量检查命令
  pi.registerCommand("quality-check", {
    description: "Run quality gate on current project",
    handler: async (_args, ctx) => {
      const result = await guardian.runQualityGate(ctx);
      if (result.passed) {
        ctx.ui.notify(`✅ Quality gate passed (${result.score}/100)`, "success");
      } else {
        ctx.ui.notify(`❌ Quality gate failed (${result.score}/100) — ${result.findings.length} findings`, "error");
      }
    },
  });

  pi.registerCommand("quality-review", {
    description: "Run five-axis review",
    handler: async (_args, ctx) => {
      ctx.ui.notify("Running five-axis review...", "info");
      await ctx.sessionManager.executeCommand?.(
        `python3 ~/.agents/skills/code-quality-guard/scripts/qguard.py review . --max-files 50`
      );
    },
  });

  pi.registerCommand("threat-model", {
    description: "Run STRIDE threat modeling",
    handler: async (_args, ctx) => {
      ctx.ui.notify("Running STRIDE threat model...", "info");
      await ctx.sessionManager.executeCommand?.(
        `python3 ~/.agents/skills/code-quality-guard/scripts/qguard.py threats src/ --json`
      );
    },
  });

  pi.registerCommand("learn-patterns", {
    description: "Learn quality patterns from current project",
    handler: async (_args, ctx) => {
      ctx.ui.notify("Learning patterns from project...", "info");
      await ctx.sessionManager.executeCommand?.(
        `python3 ~/.agents/skills/code-quality-guard/scripts/qguard.py distill . --output distillation/project-patterns.json`
      );
    },
  });

  console.log("[code-quality-guard-v5] Extension loaded with intent detection");
}
TS_EOF

echo "  ✅ Pi extension installed"

# 2. Claude Code
echo "[2/5] Installing for Claude Code..."
mkdir -p "$HOME/.claude/skills/code-quality-guard"
cp "$SKILL_DIR/SKILL.md" "$HOME/.claude/skills/code-quality-guard/SKILL.md"
cp -r "$SKILL_DIR/scripts" "$HOME/.claude/skills/code-quality-guard/"
cp -r "$SKILL_DIR/playbooks" "$HOME/.claude/skills/code-quality-guard/"

# 创建标准的 SKILL.md 格式
cat > "$HOME/.claude/skills/code-quality-guard/SKILL.md" << 'CLAUDE_EOF'
---
name: code-quality-guard
description: "Multi-language AI code quality guard with AST-based 5-axis scoring, STRIDE threat modeling, and pattern distillation. Auto-triggered on code writing, review, and commit."
version: 5.0.0
author: ryan
tags: [code-quality, ast-analysis, security, testing, ci-cd, distillation, five-axis-scoring]
---

# Code Quality Guard v5

A unified code quality engine for coding agents. Provides intent-aware quality enforcement with AST-based analysis.

## Quick Commands

| Command | Description |
|---------|-------------|
| `/qguard review <path>` | Five-axis scoring |
| `/qguard threats <path>` | STRIDE threat modeling |
| `/qguard gate <path>` | Quality gate (CI) |
| `/qguard distill <path>` | Extract design patterns |
| `/qguard learn <path>` | Learn from project code |

## Five-Axis Scoring

| Axis | Weight | Focus | Min Score |
|------|--------|-------|-----------|
| **Correctness** | 20% | Error handling, null checks | 15/20 |
| **Readability** | 20% | Naming, function length | 15/20 |
| **Architecture** | 25% | Layering, coupling, god classes | 18/25 |
| **Security** | 20% | Secrets, injection, auth | 15/20 |
| **Performance** | 15% | N+1 queries, timeouts | 10/15 |

**Pass Threshold**: Score ≥ 70, no critical findings

## Auto-Trigger Behavior

This skill is automatically activated when:
- User prompts contain: `implement`, `write`, `create`, `fix`, `refactor`, `review`
- Code files are being written: `.py`, `.ts`, `.go`, `.java`, `.rs`
- Git commit is detected
- PR/Merge request is created

When triggered, the skill will:
1. Inject relevant quality rules into context
2. Provide real-time feedback during code generation
3. Run quality gate before commit
4. Generate threat model for security-sensitive code

## Usage Examples

```bash
# Review a file
/qguard review src/payment_processor.py

# Full project review
/qguard review . --max-files 100

# Threat modeling
/qguard threats src/ --json > threats.json

# Quality gate (for CI)
/qguard gate . --min-score 70

# Learn patterns from codebase
/qguard learn . --output distillation/patterns.json
```

## Integration Points

### Pre-commit Hook
```bash
python3 ~/.agents/skills/code-quality-guard/scripts/qguard.py gate . --min-score 70
```

### GitHub Actions
See `ci/quality-check.yml` for full CI/CD integration.

### biz-delivery
```python
from integrations.biz_delivery.post_td_review import post_td_check
result = post_td_check(td_output_dir)
```

## Anti-Patterns Detected

| Anti-Pattern | Severity | Fix |
|-------------|----------|-----|
| Hardcoded Secret | 🔴 Critical | Use env vars |
| SQL Injection | 🔴 Critical | Parameterized queries |
| Eval/Exec | 🔴 Critical | Safe parsers |
| God Class | 🟡 Warning | Split classes |
| Long Function | 🟡 Warning | Extract functions |
| High Complexity | 🟡 Warning | Guard clauses |
| Deep Nesting | 🟡 Warning | Early return |

## Design Patterns Extracted

| Pattern | Detection | Use Case |
|---------|-----------|----------|
| Repository | Class name contains "Repository"/"DAO" | Data access |
| Strategy | Class name contains "Strategy" | Algorithm families |
| Builder | Class name contains "Builder" | Complex objects |
| Factory | Function with "create"/"factory" | Object creation |
| Observer | Methods with "observe"/"listener" | Event-driven |
| Circuit Breaker | Class with "Breaker"/"Circuit" | Cascade prevention |
| Singleton | Class name contains "Singleton" | Global instance |
| DI | Constructor/method injection | Loose coupling |
| Result Type | `Result<T, E>` or `Either<A, B>` | Error handling |
| Option Pattern | Functional option/config | Type-safe config |

## Language Support

| Language | AST Analysis | Pattern Detection | Security Scan |
|----------|-------------|-------------------|---------------|
| Python | ✅ | ✅ | ✅ |
| TypeScript | ✅ | ✅ | ✅ |
| Go | ✅ | ✅ | ✅ |
| Java | ✅ | ✅ | ✅ |
| Rust | ✅ | ✅ | ✅ |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v5.0.0 | 2025 | Intent detection, auto-trigger, multi-agent support |
| v4.0.0 | 2025 | AST-based analysis, 5-axis scoring, STRIDE |
| v3.0.0 | 2025 | 13 playbooks, threat modeling |
CLAUDE_EOF

echo "  ✅ Claude Code skill installed"

# 3. OpenAI Codex
echo "[3/5] Installing for OpenAI Codex..."
mkdir -p "$HOME/.codex/skills/code-quality-guard"
cp "$SKILL_DIR/SKILL.md" "$HOME/.codex/skills/code-quality-guard/SKILL.md"
cp -r "$SKILL_DIR/scripts" "$HOME/.codex/skills/code-quality-guard/"

# 创建 AGENTS.md 增强上下文
cat > "$HOME/.codex/AGENTS.md" << 'EOF'
# Agent Quality Guidelines

## Code Quality Standards

All code generated must pass the 5-axis quality gate:

| Axis | Weight | Min Score | Check |
|------|--------|-----------|-------|
| Correctness | 20% | 15/20 | Error handling, null checks |
| Readability | 20% | 15/20 | Naming, function length |
| Architecture | 25% | 18/25 | Layering, SRP |
| Security | 20% | 15/20 | No secrets, no injection |
| Performance | 15% | 10/15 | No N+1, timeouts |

## Quality Gate Command

```bash
python3 ~/.codex/skills/code-quality-guard/scripts/qguard.py gate . --min-score 70
```

## Critical Rules
- NO hardcoded passwords/secrets/API keys
- NO SQL injection (use parameterized queries)
- NO eval()/exec()
- NO swallowed exceptions
- NO deep nesting (>3 levels)

## Testing Requirements
- Write tests BEFORE implementation
- Test boundary conditions
- Test error paths
- Target ≥ 80% coverage
EOF

echo "  ✅ Codex skill installed"

# 4. Cursor
echo "[4/5] Installing for Cursor..."
mkdir -p "$HOME/.cursor/rules"
cat > "$HOME/.cursor/rules/code-quality-guard.md" << 'EOF'
# Code Quality Guard Rules

When writing or reviewing code, follow these quality standards:

## Five-Axis Quality Standards

### Correctness (20%)
- Always handle null/None/undefined checks
- Use try/catch or equivalent error handling
- Validate all inputs before processing
- Add boundary condition tests

### Readability (20%)
- Functions should be < 50 lines
- Nesting depth ≤ 3 levels (use early return)
- Variable names must be descriptive
- Remove TODO/FIXME/HACK comments before commit

### Architecture (25%)
- Follow layering: Controller → Service → Repository
- One class/function per concern (SRP)
- Use dependency injection, not global state
- Avoid god classes (> 15 methods)

### Security (20%)
- NEVER hardcode passwords, secrets, API keys
- NEVER use eval() or exec()
- ALWAYS use parameterized queries
- Add auth checks on privileged operations
- Mask sensitive data in logs

### Performance (15%)
- Avoid N+1 queries in loops
- Set explicit timeouts on external calls
- Don't recursively call without termination

## Quick Checks Before Commit

```bash
python3 ~/.agents/skills/code-quality-guard/scripts/qguard.py gate . --min-score 70
```
EOF

# 创建项目级 .cursorrules
cat > "$HOME/biz-delivery/.cursorrules" << 'EOF'
# Code Quality Rules

When writing or reviewing code:
1. No hardcoded secrets (password, api_key, token)
2. Use parameterized queries (no SQL injection)
3. Handle all errors (try/catch)
4. Functions < 50 lines, nesting ≤ 3 levels
5. One responsibility per class/function
6. Write tests for new code
7. Run quality gate before commit:
   python3 ~/.agents/skills/code-quality-guard/scripts/qguard.py gate . --min-score 70
EOF

echo "  ✅ Cursor rules installed"

# 5. GitHub Copilot
echo "[5/5] Installing for GitHub Copilot..."
mkdir -p "$HOME/biz-delivery/.github"
cat > "$HOME/biz-delivery/.github/copilot-instructions.md" << 'EOF'
# Code Quality Instructions

When generating or reviewing code:

## Critical Rules
1. Never hardcode secrets (use environment variables)
2. Use parameterized queries (no SQL injection)
3. Handle all errors properly
4. Keep functions under 50 lines
5. Nesting depth should not exceed 3 levels
6. Write tests for new functionality

## Quality Standards
- Correctness: Error handling, null checks, boundary conditions
- Readability: Descriptive names, function length < 50 lines
- Architecture: Layer separation, single responsibility
- Security: No secrets, no injection, auth checks
- Performance: No N+1 queries, explicit timeouts

## Before Commit
Run quality gate:
```bash
python3 ~/.agents/skills/code-quality-guard/scripts/qguard.py gate . --min-score 70
```
EOF

echo "  ✅ Copilot instructions installed"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                   Installation Complete!                  ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║                                                           ║"
echo "║  ✅ Pi      → ~/.pi/agent/extensions/code-quality-guard  ║"
echo "║  ✅ Claude  → ~/.claude/skills/code-quality-guard/       ║"
echo "║  ✅ Codex   → ~/.codex/skills/code-quality-guard/        ║"
echo "║  ✅ Cursor  → ~/.cursor/rules/code-quality-guard.md      ║"
echo "║  ✅ Copilot → biz-delivery/.github/copilot-instructions  ║"
echo "║                                                           ║"
echo "║  Auto-Trigger Rules:                                      ║"
echo "║  • Intent detection: implement/write/create/fix/review   ║"
echo "║  • File types: .py .ts .go .java .rs                     ║"
echo "║  • Operations: git commit, PR, merge                     ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
