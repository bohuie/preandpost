# Cross-Reference Table

| Metric / Concept | SonarQube Local Scanner | Beyond the Pull Request | Pre-Post AI Comparisons | Status | Notes / Limitation |
|---|---|---|---|---|---|
| **Security Domain** |  |  |  |  |  |
| Vulnerabilities | ✅ | ✅ | ✅ Discussed as AI-code risk | **Covered** | To see if post-GenAI code has more potential security issues. |
| Security Rating | ✅ | Not shown | Not directly | - | - |
| Security Remediation Effort | ✅ | Not shown | Not directly | - | - |
| **Reliability Domain** |  |  |  |  |  |
| Bugs | ✅ | ✅ | ✅ discussed as AI-code risk | **Covered** | Measuring potential bugs/errors. |
| Reliability Rating | ✅ | ✅ | Not directly | **Covered** | Static reliability, not real bugs at runtime. |
| Reliability Remediation Effort | ✅ | Not shown | Not directly | - | - |
| **Maintainability Domain** |  |  |  |  |  |
| Maintainability Rating | ✅ | ✅ | Conceptually related | **Covered** | Can be related to branch naming or PR feature size. |
| Code Smells | ✅ | ✅ | ✅ related to code style/fingerprint | **Covered** | For viewing maintainability issues. |
| Debt | ✅ | Not shown | Not directly | - | - |
| Debt Ratio | ✅ | Not shown | Not directly | - | - |
| **Security Review Domain** |  |  |  |  |  |
| Security Hotspots | ✅ | Not shown | Not directly | - | - |
| Security Review Rating | ✅ | Not shown | Not directly | - | - |
| Hotspots Reviewed | ✅ | Not shown | Not directly | - | - |
| **Coverage Domain** |  |  |  |  |  |
| Lines to Cover | ✅ | Not shown | ✅ testing-related | **Partially covered** | Can show parts of code that are eligible for testing. |
| Uncovered Lines | ✅ | Not shown | ✅ testing-related | **Partially covered** | - |
| Line Coverage | ✅ | Not shown | ✅ testing habits | **Partially covered** | For testing analysis if test runner/report is available. |
| **Duplications Domain** |  |  |  |  |  |
| Duplication Density | ✅ | Not shown | ✅ related | **Covered** | To calculate DRY violations. |
| Duplicated Lines | ✅ | Not shown | ✅ related | **Covered** | To see if AI-era code is more repetitive. |
| Duplicated Blocks | ✅ | Not shown | ✅ related | **Covered** | Indicator for repeated logic. |
| Duplicated Files | ✅ | Not shown | ✅ related | **Covered** | Can be influenced by template/framework files, so filtering is necessary. |
| **Size Domain** |  |  |  |  |  |
| Lines of Code / ncloc | ✅ | ✅ | Not directly | - | - |
| Lines | ✅ | Not shown | Not directly | - | - |
| Statements | ✅ | Not shown | Not directly | - | - |
| Functions | ✅ | Not shown | Not directly | - | - |
| Classes | ✅ | Not shown | Not directly | - | - |
| Files | ✅ | Not shown | PR/file-level related | - | SonarQube Files = total analyzed files, not Files Changed in PR. |
| Comment Lines | ✅ | Not shown | ✅ documentation/comment density | **Covered** | Can measure comment density, but does not assess whether comments are meaningful. |
| Comments (%) | ✅ | Not shown | Not directly | - | - |
| **Complexity Domain** |  |  |  |  |  |
| Cyclomatic Complexity / Complexity | ✅ | ✅ | ✅ related | **Covered** | Measures the number of logic paths. |
| Cognitive Complexity | ✅ | ✅ | ✅ related | **Covered** | Closer to human readability/understandability. |
| **Issues Domain** |  |  |  |  |  |
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