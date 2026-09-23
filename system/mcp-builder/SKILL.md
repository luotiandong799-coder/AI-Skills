---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).、工具过载、上下文爆、按需加载、渐进式发现、search_tools、catalog/inspect/execute、阈值切换、服务器按需连、代码模式、组合调用、沙箱执行、逐次授权、跨 server 不可信、MCP 调试、Inspector、stdio 日志、协议协商、server/discover、_meta 字段、-32022、-32602、-32021、启动路径
license: Complete terms in LICENSE.txt、三原语、工具资源提示、反模式、巨型服务器、批量变体、什么时候不该用、stdio、Streamable HTTP、无状态默认、会话头、OAuth 2.1、受众绑定、签发者、细粒度范围、一次性补齐、握手是契约、协议错误、工具执行错误、isError、可重试标记、建议动作
version: 1.1.0
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations. Performance varies by client—some clients benefit from code execution that combines basic tools, while others work better with higher-level workflows. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data. Some clients support code execution which can help agents filter and process data efficiently.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap to find relevant pages: `https://modelcontextprotocol.io/sitemap.xml`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK support and good compatibility in many execution environments e.g. MCPB. Plus AI models are good at generating TypeScript code, benefiting from its broad usage, static typing and good linting tools)
- **Transport**: Streamable HTTP for remote servers, using stateless JSON (simpler to scale and maintain, as opposed to stateful sessions and streaming responses). stdio for local servers.

**Load framework documentation:**

- **MCP Best Practices**: [📋 View Best Practices](./reference/mcp_best_practices.md) - Core guidelines

**For TypeScript (recommended):**
- **TypeScript SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - TypeScript patterns and examples

**For Python:**
- **Python SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python Guide](./reference/python_mcp_server.md) - Python patterns and examples

#### 1.4 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication requirements, and data models. Use web search and WebFetch as needed.

**Tool Selection:**
Prioritize comprehensive API coverage. List endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

See language-specific guides for project setup:
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - Project structure, package.json, tsconfig.json
- [🐍 Python Guide](./reference/python_mcp_server.md) - Module organization, dependencies

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions
- Add examples in field descriptions

**Output Schema:**
- Define `outputSchema` where possible for structured data
- Use `structuredContent` in tool responses (TypeScript SDK feature)
- Helps clients understand and process tool outputs

**Tool Description:**
- Concise summary of functionality
- Parameter descriptions
- Return type schema

**Implementation:**
- Async/await for I/O operations
- Proper error handling with actionable messages
- Support pagination where applicable
- Return both text content and structured data when using modern SDKs

**Annotations:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**TypeScript:**
- Run `npm run build` to verify compilation
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

**Python:**
- Verify syntax: `python -m py_compile your_server.py`
- Test with MCP Inspector

See language-specific guides for detailed testing approaches and quality checklists.

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

**Load [✅ Evaluation Guide](./reference/evaluation.md) for complete evaluation guidelines.**

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

To create effective evaluations, follow the process outlined in the evaluation guide:

1. **Tool Inspection**: List available tools and understand their capabilities
2. **Content Exploration**: Use READ-ONLY operations to explore available data
3. **Question Generation**: Create 10 complex, realistic questions
4. **Answer Verification**: Solve each question yourself to verify answers

#### 4.3 Evaluation Requirements

Ensure each question is:
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls and deep exploration
- **Realistic**: Based on real use cases humans would care about
- **Verifiable**: Single, clear answer that can be verified by string comparison
- **Stable**: Answer won't change over time

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# Reference Files

## 📚 Documentation Library

Load these resources as needed during development:

### Core MCP Documentation (Load First)
- **MCP Protocol**: Start with sitemap at `https://modelcontextprotocol.io/sitemap.xml`, then fetch specific pages with `.md` suffix
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - Universal MCP guidelines including:
  - Server and tool naming conventions
  - Response format guidelines (JSON vs Markdown)
  - Pagination best practices
  - Transport selection (streamable HTTP vs stdio)
  - Security and error handling standards

### SDK Documentation (Load During Phase 1/2)
- **Python SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- **TypeScript SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

### Language-Specific Implementation Guides (Load During Phase 2)
- [🐍 Python Implementation Guide](./reference/python_mcp_server.md) - Complete Python/FastMCP guide with:
  - Server initialization patterns
  - Pydantic model examples
  - Tool registration with `@mcp.tool`
  - Complete working examples
  - Quality checklist

- [⚡ TypeScript Implementation Guide](./reference/node_mcp_server.md) - Complete TypeScript guide with:
  - Project structure
  - Zod schema patterns
  - Tool registration with `server.registerTool`
  - Complete working examples
  - Quality checklist

### Evaluation Guide (Load During Phase 4)
- [✅ Evaluation Guide](./reference/evaluation.md) - Complete evaluation creation guide with:
  - Question creation guidelines
  - Answer verification strategies
  - XML format specifications
  - Example questions and answers
  - Running an evaluation with the provided scripts

## 工具过载：渐进式发现优于一次性全量注入（来源：MCP 官方 docs.modelcontextprotocol.io client-best-practices，2026-09-23 r150 续跑独立实拉首读，清单外新信源）

- **工具定义占上下文超过阈值就切换加载策略**：当已连接服务的工具定义撑满上下文窗口的 1%–5% 时，从"启动时全量注入"切到"按需发现"。判据：一个 agent 暴露几百个工具时，把所有 tool schema 一次性塞进 context 是反模式——浪费 token、拖慢、降质。
- **三层 catalog/inspect/execute**：① 只暴露一个轻量 `search_tools` 元工具，返回名称+一行描述；② 模型选定后 `get_tool_details` 才拉全量 schema；③ 拿到完整接口后再调用，中间结果不进 context。
- **发现策略按场景选**：关键词(BM25/regex) / 向量(语义) / 子代理(小模型选型) / 混合。平台自带 tool-search 时优先用平台能力，只在需要领域排序或权限过滤时才自建。
- **服务器也按需连**：维护 server 注册表，`enable_server` 才连、`disable_server` 释放上下文；通用 agent 起步只挂少量常驻 server。
- 与 §代码模式 的分工：本条管"工具定义怎么进 context"；§代码模式 管"多工具调用结果怎么不流经 context"。

## 组合式工具调用：代码模式把中间结果挡在 context 外（来源：MCP 官方 client-best-practices，2026-09-23 r150 续跑独立实拉首读，清单外新信源）

- **链式多工具调用改写成代码，在沙箱里跑，只回传最终摘要**：模型不再逐步调工具、把每个中间结果灌进 context，而是写一段脚本调 typed stub，沙箱执行、只把 `console.log` 的最终一行返回模型。示例：从日志筛错误→逐个建工单，几千条日志不进 context。
- **沙箱三件套隔离**：① 无直接网络（所有外部通信经 host broker 转发，broker 做鉴权）；② 凭证由 host 持有，生成代码只调 typed 函数；③ 设超时/内存上限防失控。
- **授权是逐次而非一次性**：批准脚本 ≠ 批准它运行时每个工具调用；broker 对每个调用仍按授权策略评估（可"本脚本内允许 X"的归类批准，但必须逐个评估）。跨 server 数据时，一 server 的结果是另一 server 的不可信输入，broker 对转发调用同样做输入审查，光截断输出拦不住外泄。
- **错误处理**：MCP 工具错误以 `isError:true` 的成功响应返回，包装层应转成异常让模型 try/catch；脚本未捕获的错作为结果返回，让模型自纠并负责已提交的副作用。
- 与 §渐进式发现 的分工：那条管"定义进不进 context"；本条管"调用结果过不过 context"。

## 接协议类工具先上 Inspector，再看握手字段（来源：MCP 官方 docs.modelcontextprotocol.io/tools/debugging，2026-09-23 r150 续跑独立实拉首读，清单外新信源）

- **调试 MCP 集成的第一站是 Inspector**：传输无关的交互式测试 UI，连 stdio 或 Streamable HTTP，调 tools/prompts/resources、看通知流。先它，再上客户端日志。
- **日志落到 stderr（stdio 传输）**：本地 server 不要往 stdout 写日志（会干扰协议）；重要事件记启动步骤/资源访问/工具执行/错误/性能指标。Streamable HTTP 下 stderr 不被客户端捕获，改用服务端聚合或 OpenTelemetry。
- **排障先看握手与协商字段**：① 协议版本不兼容 → 调 `server/discover` 看支持版本，不匹配报 `UnsupportedProtocolVersionError(-32022)`；② 每个请求必须带 `_meta` 的 `protocolVersion` 与 `clientCapabilities`（否则 `-32602` Invalid params）；③ server 要的能力客户端没声明 → `MissingRequiredClientCapabilityError(-32021)`。先核 `_meta` 与 `server/discover` 两端声明。
- **常见启动坑**：command 用绝对路径（stdio server 的工作目录可能未定义）；env 只继承受限子集，缺变量显式在配置里给；JSON 非法/缺字段/类型不符是高频原因。
- 与通用排障循环的分工：复现→最小化→假设→验证 管通用循环；本条管"接 MCP/协议类工具"这一子类特有的第一站与握手判据。


## 服务器侧三原语各管一件事，混用会同时带来上下文污染与副作用风险（来源：GingerLabs 2026-06-20 + TECHTAEK 2026-04-23，2026-09-24 豆包 r159-B 实拉取证，WB 审计属实后落地）
- **★三种原语是三种语义，不是三种写法**：工具 = 动作层（模型可以调用的可执行函数）；资源 = 可寻址的上下文（按需取用）；提示 = 用户显式选择才加载的工作流模板。判据：**把"读数据"做成工具，就把它变成了模型可能随手触发的副作用**；把"模板"塞进系统指令，用户就失去了选择权。
- **★四条反模式**：不要把一切都做成工具；不要把每份文档都塞进默认上下文（提示污染）；不要把提示模板当隐藏的系统指令；**不要做一个描述整个业务的巨型服务器**。判据：**好服务器的判据是"给 agent 刚够行动的能力、给 host 刚够取用的结构"**，覆盖面是坏指标。


## 工具描述要回答"什么时候不该用我"，输入验证不是可选项（来源：Axiom Studio 2026-04-04，2026-09-24 豆包 r159-B 实拉取证）
- **★描述里必须写清边界**：什么情况该用我、**什么情况该用别的**；每个参数写合法值与格式；把大小限制、允许取值这类约束直接写进描述。判据：**只写"能做什么"的描述会让模型在错的场景里也调用它**。
- **★成环的常见操作要提供批量变体**：模型在循环里反复调用同一个单条接口，是成本与限流的主要来源。判据：**提供一个批量入口，比在提示里劝它"一次多做几个"有效得多**。
- **★所有输入先验证再使用**：路径穿越、注入一类的校验是服务器自己的责任，不能指望调用方守规矩。判据：**信任调用方的输入校验等于没有校验**。


## 传输只有两个标准绑定，远程默认无状态（来源：MCP 官方 `modelcontextprotocol.io/specification/2026-07-28/basic/transports`（2026-09-24 WB 审计实测：标准绑定仅 stdio 与 Streamable HTTP 两项，旧版 SSE 会话形态归入向后兼容）+ DEV 2026-09-21 + MCPgee 2026-09-17 + AWS 2026-09-01 stateless 指南，2026-09-24 豆包 r159-B 实拉取证，审计属实后落地）
- **★本地与远程是两条不同的路**：stdio 是客户端把服务器当子进程、用标准流通信，零基础设施、零网络配置、隔离性最好，适合命令行/桌面/本地开发；**其余一切走 Streamable HTTP**——单个 POST 端点，每个响应可以是 JSON 对象也可以是该请求范围内的 SSE 流，**客户端必须两种都能吃**。判据：**按"是否需要跨网络/跨进程复用"选，不按个人习惯选**。
- **★旧的 HTTP+SSE 传输已废弃，要迁**：现行规范只列了两个标准绑定，旧形态只在向后兼容里保留。判据：**"还能连上"不代表还在规范内**——新实现不要照着旧示例写。
- **★无状态是默认，不是可选项**：会话状态要移出进程内存，用会话标识头管理；长耗时工具的状态落外部存储；无服务器环境下用无状态模式。判据：**把会话放在进程内存里，等于把"能不能扩容"和"会不会丢"绑在一起**。


## 授权按 OAuth 2.1 走，token 每次都要验证三件事（来源：MCP 官方 `modelcontextprotocol.io/specification/2026-07-28/basic/authorization`（2026-09-24 WB 审计实测原文：基于 OAuth 2.1 draft-ietf-oauth-v2-1-13、RFC8707 资源指示、RFC9207 签发者标识、RFC9728 受保护资源元数据）+ DeepWiki 2026-07-09 + NerdLevelTech 2026-05-14，2026-09-24 豆包 r159-B 实拉取证）
- **★HTTP 传输下受保护资源服务器就是 OAuth 2.1 资源服务器**：规范列出的依赖包括 OAuth 2.1 草案、承载令牌用法、授权服务器元数据、动态客户端注册、资源指示、受保护资源元数据、签发者标识。判据：**自建一套"看着像 OAuth"的流程，会把这些已经解决过的攻击面重新踩一遍**。
- **★每一次请求都要验三件事**：令牌是不是发给**本服务器**的（受众绑定，靠资源指示参数实现）、签发者对不对（签发者标识比对，且**不做大小写折叠、默认端口省略、尾部斜杠之类的归一化**）、权限范围够不够。判据：**只验"签名有效"会接受一张发给别的服务的令牌**。
- **★权限范围要细，不足时整体补齐而不是一次给一个**：用读写分离的细粒度范围而不是一个全通范围；服务端在 401/403 挑战里回所需范围，且要**一次性把本次操作所需的范围全给出来**，逐个挤牙膏式地挑战会逼着客户端反复走授权流程。判据：**范围切得粗，一次越权就是全部失守；挑战切得碎，用户体验被流程本身拖垮**。
- **★客户端取新范围时要做并集**：重新授权时把之前已 granted 的范围并上，否则会丢掉其它操作还需要的能力。判据：**"补权限"补成了"换权限"，是 step-up 流程最常见的自伤**。


## 握手是契约，错误要分两层，工具错误还得自带恢复信息（来源：MCP 官方 `specification/2026-07-28/server/tools`（2026-09-24 WB 审计实测原文：协议错误为 JSON-RPC error code -32602，工具执行错误为 result 内 isError:true）+ arXiv 2603.13417 + IETF draft-pelov-bounded-agent-capabilities 2026-07-03，2026-09-24 豆包 r159-B 实拉取证）
- **★初始化握手要验证协议版本，不兼容就报错，不要静默降级**。判据：**静默降级会把不兼容推迟成一次说不清的怪行为**。
- **★两类错误的处理方式相反**：协议错误（未知工具、畸形请求、服务端故障）走 JSON-RPC 错误码，模型基本修不了；**工具执行错误放在结果体里并置错误标记，里面要写清"哪里不对"，因为这一类模型能改参数重试**。判据：**把可修复的错误扔进协议错误，等于主动放弃模型的自纠正能力**。
- **★工具错误要自带可重试标记与建议动作**：现行工具错误没有错误码结构，无法声明是否可重试、是否部分成功、副作用是否已经发生；因此在文本里显式给出"能不能重试"和"下一步该干什么"。判据：**缺了可重试标记，调用方只能在"盲目重试"和"一律放弃"之间二选一**。
- **★错误消息要区分"重试安全"与"副作用已发生"**：已经落地的副作用不能靠重试来"修正"。判据：**不区分这两者，重试会把一次失败变成两次副作用**。
