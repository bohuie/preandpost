# **Appendix of SonarQube Metrics Definition**
Link: https://docs.sonarsource.com/sonarqube-server/9.8/user-guide/metric-definitions

| Metric | Description |
|---|---|
| **🟨 Security** | Issues in this domain mark potential weaknesses to hackers. |
| Vulnerabilities | Number of vulnerabilities. |
| Security Rating | A–E rating based on the severity of detected vulnerabilities. |
| Remediation Effort | Estimated time required to fix all detected vulnerability issues. |
| **🟦 Reliability** | Issues in this domain mark code where behavior may differ from what was expected. |
| Bugs | Number of bugs. |
| Reliability Rating | Ordinal reliability ranking. |
| Remediation Effort | Estimated time required to fix all reliability issues or bugs. |
| **🟪 Maintainability** | Issues in this domain mark code that will be more difficult to update competently than it should. |
| Maintainability Rating | Ordinal maintainability ranking. |
| Code Smells | Number of code smells. |
| Debt | Estimated effort to fix all code smells. |
| Debt Ratio | Ratio between the estimated cost to fix maintainability issues and the estimated cost to develop the code. |
| **🟦 Security Review** | This domain represents potential security risks in the form of hotspots and their review status. |
| Security Hotspots | Number of security-sensitive code areas that need to be reviewed to determine whether they are safe or require a fix. |
| Security Review Rating | A–E rating based on the percentage of security hotspots that have been reviewed. |
| Hotspots Reviewed | Percentage of reviewed security hotspots compared to the total number of security hotspots. |
| **🟧 Coverage** | Measures how much of the code is covered by tests. |
| Lines to Cover | Number of lines of code that could be covered by unit tests. Blank lines or full comment lines are not counted. |
| Uncovered Lines | Number of lines or conditions that are not covered by unit tests. |
| Line Coverage | Percentage of lines executed during unit tests. |
| **🟪 Duplications** | Measures duplicated code in the codebase. |
| Density | Percentage of duplicated lines in the codebase. Formula: `duplicated_lines / lines_of_code * 100`. |
| Duplicated Lines | Number of lines involved in duplications. |
| Duplicated Blocks | Number of duplicated blocks of lines. |
| Duplicated Files | Number of files involved in duplications. |
| **🟦 Size** | Measures the size and structure of the codebase. |
| Lines of Code | Number of physical lines that contain at least one character and are not whitespace, tabs, or comments. |
| Lines | Number of physical lines. |
| Statements | Number of statements. |
| Functions | Number of functions. Depending on the language, a function may be defined as a function, method, or paragraph. |
| Classes | Number of classes, including nested classes, interfaces, enums, and annotations. |
| Files | Number of files. |
| Comment Lines | Number of lines containing comments or commented-out code. |
| Comments (%) | Comment line density. Formula: `comment_lines / (lines_of_code + comment_lines) * 100`. |
| **🟩 Complexity** | Measures how simple or complicated the control flow of the application is. |
| Cyclomatic Complexity / Complexity | Number of linearly independent paths through the code. Each function has a minimum complexity of 1, and the value increases when the control flow splits. |
| Cognitive Complexity | Measures how difficult the code’s control flow is to understand. |
| **🟥 Issues** | Counts issues by severity level. |
| Blocker Issues | Number of blocker severity issues. |
| Critical Issues | Number of critical severity issues. |
| Major Issues | Number of major severity issues. |
| Minor Issues | Number of minor severity issues. |

# Cross-Reference Table

| Metric / Concept | SonarQube Local Scanner | Beyond the Pull Request | Pre-Post AI Comparisons | Status | Notes / Limitation |
|---|---|---|---|---|---|
| **Security Domain** | ✅ | ✅ | Partially discussed | **Covered** | For spotting potential security weaknesses. |
| Vulnerabilities | ✅ | ✅ | ✅ Discussed as AI-code risk | **Covered** | To see if post-GenAI code has more potential security issues. |
| Security Rating | ✅ | Not shown | Not directly | - | - |
| Security Remediation Effort | ✅ | Not shown | Not directly | - | - |
| **Reliability Domain** | ✅ | ✅ | Partially discussed | **Covered** | - |
| Bugs | ✅ | ✅ | ✅ discussed as AI-code risk | **Covered** | Measuring potential bugs/errors. |
| Reliability Rating | ✅ | ✅ | Not directly | **Covered** | Static reliability, not real bugs at runtime. |
| Reliability Remediation Effort | ✅ | Not shown | Not directly | - | - |
| **Maintainability Domain** | ✅ | ✅ | ✅ Conceptually related | **Covered** | To connect SonarQube with the quality of student code. |
| Maintainability Rating | ✅ | ✅ | Conceptually related | **Covered** | Can be related to branch naming or PR feature size. |
| Code Smells | ✅ | ✅ | ✅ related to code style/fingerprint | **Covered** | For viewing maintainability issues. |
| Debt | ✅ | Not shown | Not directly | - | - |
| Debt Ratio | ✅ | Not shown | Not directly | - | - |
| **Security Review Domain** | ✅ | Not shown | Not directly | - | - |
| Security Hotspots | ✅ | Not shown | Not directly | - | - |
| Security Review Rating | ✅ | Not shown | Not directly | - | - |
| Hotspots Reviewed | ✅ | Not shown | Not directly | - | - |
| **Coverage Domain** | ✅ | Not shown | ✅ testing-related | **Partially covered** | If the test coverage report is integrated. |
| Lines to Cover | ✅ | Not shown | ✅ testing-related | **Partially covered** | Can show parts of code that are eligible for testing. |
| Uncovered Lines | ✅ | Not shown | ✅ testing-related | **Partially covered** | - |
| Line Coverage | ✅ | Not shown | ✅ testing habits | **Partially covered** | For testing analysis if test runner/report is available. |
| **Duplications Domain** | ✅ | ✅ Duplicate tags/issues | ✅ DRY violation | **Covered** | Pre-Post AI fingerprint. |
| Duplication Density | ✅ | Not shown | ✅ related | **Covered** | To calculate DRY violations. |
| Duplicated Lines | ✅ | Not shown | ✅ related | **Covered** | To see if AI-era code is more repetitive. |
| Duplicated Blocks | ✅ | Not shown | ✅ related | **Covered** | Indicator for repeated logic. |
| Duplicated Files | ✅ | Not shown | ✅ related | **Covered** | Can be influenced by template/framework files, so filtering is necessary. |
| **Size Domain** | ✅ | ✅ | PR size/code size related | - | SonarQube gives repo/file size, but not PR-level size. |
| Lines of Code / ncloc | ✅ | ✅ | Not directly | - | - |
| Lines | ✅ | Not shown | Not directly | - | - |
| Statements | ✅ | Not shown | Not directly | - | - |
| Functions | ✅ | Not shown | Not directly | - | - |
| Classes | ✅ | Not shown | Not directly | - | - |
| Files | ✅ | Not shown | PR/file-level related | - | SonarQube Files = total analyzed files, not Files Changed in PR. |
| Comment Lines | ✅ | Not shown | ✅ documentation/comment density | **Covered** | Can measure comment density, but does not assess whether comments are meaningful. |
| Comments (%) | ✅ | Not shown | Not directly | - | - |
| **Complexity Domain** | ✅ | ✅ | ✅ related | **Covered** | - |
| Cyclomatic Complexity / Complexity | ✅ | ✅ | ✅ related | **Covered** | Measures the number of logic paths. |
| Cognitive Complexity | ✅ | ✅ | ✅ related | **Covered** | Closer to human readability/understandability. |
| **Issues by Severity** | ✅ | ✅ | Not directly | - | - |
| Blocker Issues | ✅ | ✅ | Not directly | - | - |
| Critical Issues | ✅ | ✅ | Not directly | - | - |
| Major Issues | ✅ | ✅ | Not directly | - | - |
| Minor Issues | ✅ | ✅ | Not directly | - | - |
| Total Issues | ✅ | ✅ | Not directly | - | - |
| Confirmed Issues | ✅ | Not shown | Not directly | - | - |
| False Positive Issues | ✅ | Not shown | Not directly | - | - |
| Accepted Issues | ✅ | Not shown | Not directly | - | - |

# Missing Metrics

| Metric / Concept | Available in SonarQube? | Data Source Needed | Notes |
|---|---|---|---|
| **Beyond Pull Request** |  |  |  |
| Time to Close | ❌ | GitHub API | Measures how long a PR was processed before being closed or merged. |
| Additions | ❌ | GitHub API | Number of lines added in a PR. |
| Deletions | ❌ | GitHub API | Number of lines removed in a PR. |
| Changes | ❌ | GitHub API | Size of the PR change, usually calculated as additions + deletions or changed lines. |
| Files Changed | ❌ | GitHub API | Number of files changed in a PR. This is different from the total number of files reported by SonarQube. |
| Reviews | ❌ | GitHub API | Number of reviews or votes on a PR. Important for an acceptance model. |
| PR Accepted / Merged | ❌ | GitHub API | Response variable for the PR acceptance model. |
| PR Rejected / Closed Unmerged | ❌ | GitHub API | Needed to compare acceptance patterns. |
| Author Type: Human vs Agent | ❌ | GitHub metadata / AIDev-like dataset | SonarQube does not know whether the author is a human or an AI agent. |
| Agent Name | ❌ | GitHub metadata / external dataset | Needed to compare tools such as Copilot, Devin, Cursor, Codex, etc. |
| Task Type | ❌ | GitHub issue/PR label or manual classification | Used in Beyond PR as a predictor. |
| **Pre-Post Comparison** |  |  |  |
| Meaningful Branch Naming | ❌ | GitHub API / branch names | SonarQube does not read branch names for this type of workflow analysis. |
| One Feature per Branch | ❌ | GitHub PR/branch analysis | PR size can be observed, but SonarQube cannot determine the number of features in a branch. |
| PR Size | ❌ | GitHub API | PR size is more accurately measured using additions, deletions, and files changed. |
| Small Features per PR | ❌ | PR/commit/event log classification | Requires event logs or manual/rule-based classification. |
| Large Features per PR | ❌ | PR/commit/event log classification | Cannot be measured directly from SonarQube. |
| Refactoring Activity per PR | ❌ | Commit/PR classification | SonarQube can show quality changes, but it cannot determine whether the intent was refactoring. |
| Reviewed Merge | ❌ | GitHub API | Requires both review data and merge data. |
| Self-Merge | ❌ | GitHub API | Requires comparing the PR author with the merge actor. |
| Up-to-Date Branch | ❌ | GitHub API / Git history | Requires comparing the branch commit graph with the main branch. |
| Outdated Branch at Merge | ❌ | GitHub API / Git history | Cannot be measured from SonarQube. |
| Merge Rate | ❌ | GitHub API | SonarQube analyzes the codebase, not the PR acceptance workflow. |
| Code Churn | ❌ | Git history | Requires tracking whether lines are deleted or modified within a certain time period. |
| AI-like File-Level Score | ❌ | AI detector such as Binoculars | SonarQube is not an AI detector. |
| Team-Level AI Verdict | ❌ | AI detector + calibration | Cannot be measured from SonarQube. |
| File-Level AI Density | ❌ | AI detector + file-level scoring | Cannot be measured from SonarQube. |

# Summary
| Metric / Area | Status |
|---|---|
| Maintainability | ✅ |
| Reliability | ✅ |
| Security vulnerabilities | ✅ |
| Security hotspots | ✅ |
| Code smells | ✅ |
| Technical debt | ✅ |
| Duplication / DRY violation | ✅ |
| Complexity | ✅ |
| Cognitive complexity | ✅ |
| Size / LOC | ✅ |
| Comment density | ✅ |
| PR-level workflow | ❌ Missing |
| Branch behaviour | ❌ Missing |
| Review behaviour | ❌ Missing |
| Merge behaviour | ❌ Missing |
| AI detection / AI-like fingerprint | ❌ Missing |
| Student learning / understanding | ❌ Missing |