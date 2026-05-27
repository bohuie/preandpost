# Cross Reference Table

## Security

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Security / Vulnerabilities | **Is the rule about code that could be exploited by an attacker?** If yes, then it is a vulnerability rule.<br>- Pre-Post AI: Discusses **security vulnerabilities** as one AI-generated code looks like, e.g., insecure patterns such as SQL injection. | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Security Rating | A - E rating based on the severity of detected vulnerabilities. A = 0 Vulnerabilities, B = at least 1 Minor Vulnerability, C = at least 1 Major Vulnerability, D = at least 1 Critical Vulnerability, E = at least 1 Blocker Vulnerability. | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Bandit | A Python security static analysis tool that detects potential security issues and reports them by severity level: high, medium, and low. The metric can be computed as the change in Bandit issues before and after edits. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

### How to detect

#### Security / Vulnerabilities

1. Identify whether the code contains a pattern that can be exploited by an attacker, such as SQL injection, cross-site scripting, path traversal, hardcoded secrets, unsafe deserialization.
2. For injection vulnerabilities, trace whether untrusted external input enters the program. This input can come from user input, HTTP requests, query parameters, form fields, files.
3. Track whether that untrusted input reaches a sensitive sink, such as a SQL query execution, HTML output, shell command, file path access, or redirect URL.
4. Check whether the input is properly sanitized, validated, encoded, escaped, or parameterized before reaching the sensitive sink.
5. If untrusted input reaches a sensitive sink without proper protection, classify the issue as a vulnerability.

#### Security Rating

Security Rating is categorized based on the severity of detected vulnerabilities:

1. A = 0 Vulnerabilities.
2. B = at least 1 Minor Vulnerability.
3. C = at least 1 Major Vulnerability.
4. D = at least 1 Critical Vulnerability.
5. E = at least 1 Blocker Vulnerability.

Severity categories:

- Minor: An issue with a low impact on the application.
- Major: An issue with a medium impact on the application.
- Critical: An issue with a high impact on the application that should be fixed as soon as possible.
- Blocker: An issue that has a significant probability of severe unintended consequences on the application that should be fixed immediately.

#### Bandit

1. Collect all Python files included in the analysis.
2. Run Bandit on the selected Python files.
3. Bandit detects potential security issues, such as hardcoded secrets, unsafe subprocess calls, weak cryptography, insecure deserialization, SQL injection risks, or unsafe file handling.
4. Group the detected issues by severity level:
   - High
   - Medium
   - Low
5. Count the number of Bandit issues for each severity level.
6. If comparing pre- and post-edit code, calculate the delta for each severity level:

   `ΔBandit_s = Σ Issues_post_s(f) - Σ Issues_pre_s(f)`

   where `s ∈ {high, medium, low}`.

7. Interpret the result:
   - If `ΔBandit_s > 0`, the edits introduced more security issues at severity level `s`.
   - If `ΔBandit_s < 0`, the edits reduced security issues at severity level `s`.
   - If `ΔBandit_s = 0`, there was no change in Bandit issues for that severity level.


## Reliability

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Reliability / Bugs | **Is the rule about code that is demonstrably wrong, or more likely wrong than not?** If the answer is "yes", then it’s a bug rule. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Reliability Rating | A - E rating based on the severity of detected bugs: A = 0 bug, B = at least 1 Minor bug, C = at least 1 Major bug, D = at least 1 Critical bug, E = at least 1 Blocker bug. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### How to detect

#### Reliability / Bugs

1. Identify code patterns that are likely to produce incorrect, unexpected, or unstable behavior during execution.
2. Check whether the code violates known reliability rules, such as null/undefined values being dereferenced, conditions that are always true or always false, unreachable code, resources not being closed properly, incorrect exception handling, suspicious logic that may not behave as intended, variables used before being properly initialized.
3. Analyze the code structure using static analysis, such as control flow and data flow, to detect whether a value can reach an unsafe operation.
4. If the issue indicates code that is demonstrably wrong or very likely to fail under normal conditions, classify it as a Bug / Reliability issue.

#### Reliability Rating

Reliability Rating is categorized based on the severity of detected bugs:

1. A = 0 bugs.
2. B = at least 1 Minor bug.
3. C = at least 1 Major bug.
4. D = at least 1 Critical bug.
5. E = at least 1 Blocker bug.


## Maintainability

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Maintainability Index / Code Smells | **Is the rule neither a bug nor a vulnerability?** If yes, then it’s a code smell rule. It aggregates structural characteristics, lines of code, complexity, and comment density, into a single interpretable score where higher values denote easier maintainability. | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Debt | A measure of effort to fix all code smells, in minutes. An 8-hour day is assumed when values are shown in days, `1 day = 8 working hours`.<br>- BeyondPR: Refers to the future cost of maintaining or fixing code caused by maintainability problems such as code smells, complexity, and design compromises tags. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Debt Ratio | The ratio between the cost to develop the software and the cost to fix it. Formula: `Debt Ratio = Remediation Cost (estimated time to fix code smells) / Development Cost (cost to develop 1 line of code * Number of lines of code).`<br><br>*Cost to develop 1 line of code = 0.06 days, approximately 30 minutes. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Maintainability Rating | The rating given to the project relative to the value of the debt ratio: A = 0-0.05, B = 0.06-0.1, C = 0.11-0.20, D = 0.21-0.5, E = 0.51-1. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| NCSSMethodCount | Counts Non-Commenting Source Statements, report level in statements. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Singular Field | The scope of a field is limited to one method. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| TooManyMethods | Detects classes with too many methods. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| TooManyFields | Detects classes with too many fields. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| GodClass | Detects classes that have too many responsibilities, making the code harder to understand and maintain. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| LooseCoupling | Use interfaces instead of implementation Types. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| LawOfDemeter | Call methods from another class directly. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| AvoidReassigningParameters | Detects method/function parameters that are reassigned inside the method body. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| CollapsibleIfStmts | Detects nested if statements that can be combined into a single condition. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| PositionLiteralsFirstInComparisons | Detects comparison expressions where literal values are not placed first, such as x == 5 instead of 5 == x. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| SimplifyBooleanExpressions | Detects boolean expressions that are unnecessarily complex. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| SimplifyBooleanReturns | Detects if/else statements that return boolean values and can be simplified into a direct boolean return expression. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| SwitchStmtsShouldHaveDefault | Detects switch statements that do not include a default case. A default case helps handle unexpected or unmatched values. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| MissingBreakInSwitch | Detects switch cases that do not end with a break statement, return statement, throw statement, or another explicit control-flow exit. This can cause unintended fall-through, where execution continues into the next case. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| AvoidInstantiatingObjectsInLoops | Detects object creation inside loops. Creating new objects repeatedly in a loop can be inefficient, especially if the object could be created once outside the loop and reused. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

### How to detect

#### Maintainability / Code Smells

1. Identify whether the issue is not directly a bug and not directly a vulnerability, but still makes the code harder to understand, modify, or maintain.
2. Check whether the code violates maintainability rules, such as duplicated logic, overly complex methods, deeply nested control flow, unused variables or imports, poor naming conventions, functions/classes that are too large, confusing conditional logic, repeated code patterns, violations of coding style or standards.
3. Analyze the code structure using static analysis, such as syntax trees, control flow, and rule-based checks.
4. If the issue does not necessarily break the program now, but may make future modification harder or riskier, classify it as a Code Smell / Maintainability issue.
5. For file-level analysis, calculate a maintainability score/index for each analyzed file.
6. For repository-level analysis, compute the average maintainability across all analyzed files:

   `MI_avg = sum of maintainability scores across files / number of analyzed files`

7. If comparing two versions of the code, such as before and after a PR/commit, calculate the change in average maintainability:

   `ΔMI = MI_avg_post - MI_avg_pre`

8. Interpret the delta:
   - If ΔMI > 0, maintainability improved after the change.
   - If ΔMI < 0, maintainability decreased after the change.
   - If ΔMI = 0, maintainability stayed roughly the same.

#### NCSSMethodCount

1. Parse each method or function in the source code.
2. Count only non-commenting source statements, meaning executable or structural statements in the method.
3. Exclude: comments, blank lines, whitespace-only lines, formatting-only lines.
4. Include statements such as variable declarations, assignments, method calls, return statements, conditionals, loops, object creation.
5. Compare the method’s NCSS count against a selected threshold, e.g., 50/100.
6. If the number of non-commenting source statements exceeds the threshold, flag the method as having an NCSSMethodCount issue.

#### Singular Field

1. Parse each class and identify all class-level fields/attributes.
2. For each field, track where it is used across the class.
3. Count how many methods access or modify that field.
4. If a field is used by only one method, flag it as SingularField.
5. Check whether the field could be declared as a local variable inside that method instead of being stored as class-level state.

#### TooManyMethods

1. Parse each class in the source code.
2. Count the number of methods declared inside the class.
3. Depending on the rule configuration, exclude methods that are less relevant to class responsibility, such as getters, setters.
4. Compare the method count with a selected threshold.
5. If the class has more methods than the threshold, flag it as TooManyMethods.

#### TooManyFields

1. Parse each class in the source code.
2. Count the number of fields/attributes declared inside the class.
3. Depending on the rule configuration, exclude fields that are less relevant to class responsibility, such as constants and static final fields.
4. Compare the field count with a selected threshold.
5. If the class has more fields than the threshold, flag it as TooManyFields.

#### GodClass

1. Parse each class in the source code.
2. Measure whether the class is too large or too responsible using indicators such as number of methods, number of fields.
3. Check whether many methods in the class are unrelated or operate on different sets of fields.
4. Check whether the class controls too much system behaviour, coordinates too many other objects, or contains logic that should belong to separate classes.
5. If the class exceeds the selected rule threshold for size, flag it as GodClass.

#### LooseCoupling

1. Parse class fields, method parameters, return types, and local variable declarations.
2. Check whether the code uses a concrete implementation type when an interface or abstraction could be used instead.
3. Implementation types e.g., `ArrayList<String> names = new ArrayList<>();` or `HashMap<String, Integer> scores = new HashMap<>();`
4. Interface types e.g., `List<String> names = new ArrayList<>();` or `Map<String, Integer> scores = new HashMap<>();`
5. Flag the issue when the declared type is an implementation class, but a suitable interface type exists.

#### LawOfDemeter

1. Parse method calls in each class.
2. Look for chained method calls where an object calls a method on another object returned by a previous call.
3. Law of Demeter violations e.g., `student.getDepartment().getFaculty().getName();`

   or:

   `order.getCustomer().getAddress().getCity();`

4. These chains suggest that the current class knows too much about the internal structure of other objects.
5. A better design would ask the direct object to provide the needed information: `student.getFacultyName();`

   or:

   `order.getCustomerCity();`

6. Flag the issue when a method call reaches through another object.

#### AvoidReassigningParameters

1. Parse each method or function declaration.
2. Identify all parameters passed into the method/function.
3. Scan the method body to see whether any parameter is reassigned.
4. A reassignment can look like:

   ```java
   public void updateScore(int score) {
       score = score + 10;
   }```
In this example, score is a parameter, but it is reassigned inside the method.
5. A clearer version is to create a new local variable:
```java
public void updateScore(int score) {
    int updatedScore = score + 10;
}
```
6. Flag the issue when a parameter appears on the left-hand side of an assignment or is otherwise modified/reassigned inside the method body.

#### CollapsibleIfStmts
1. Parse the code and identify nested if statements.
2. Check whether an inner if is the only statement inside the outer if.
3. If both conditions can be safely combined without changing program behavior, flag it as CollapsibleIfStmts.

Example issue:
```java
if (user != null) {
    if (user.isActive()) {
        sendEmail(user);
    }
}
This can be simplified into:
if (user != null && user.isActive()) {
    sendEmail(user);
}
```

#### PositionLiteralsFirstInComparisons
1. Parse comparison expressions in the source code.
2. Identify comparisons involving a variable/expression and a literal value, e.g., 
numbers  (`0`, `1`, `100`), strings (`"admin"`), booleans (`true`/`false`)
null
3. Check whether the literal appears on the right side of the comparison.
4. Flag the issue when the literal is not placed first

#### SimplifyBooleanExpressions
1. Parse boolean expressions in the source code.
2. Identify expressions that contain unnecessary comparisons, redundant logic, or avoidable complexity.
3. Common examples include comparing a boolean value to true or false:
```java
if (isReady == true) {
    start();
}
```

This can be simplified to:

```java
if (isReady) {
    start();
}
```
4. Detect expressions with unnecessary negation or redundant boolean structure, such as:
```java
if (!(isReady == false)) {
    start();
}
```

This can be simplified to:

```java if (isReady) {
    start();
}
```
5. Check whether the simplification preserves the same program behavior.
6. If the expression can be simplified without changing behavior, flag it as SimplifyBooleanExpressions.

#### SimplifyBooleanReturns
1. Parse methods/functions that return a boolean value.
2. Identify if/else blocks where both branches directly return boolean literals.
3. Example issue:
```java
if (score >= 50) {
    return true;
} else {
    return false;
}
```
This can be simplified to:
```java
return score >= 50;
```
4. Also detect the opposite pattern:
```java
if (score >= 50) {
    return false;
} else {
    return true;
}
```
This can be simplified to:
```java
return score < 50;
```
5. If the boolean return can be simplified without changing behavior, flag it as SimplifyBooleanReturns.

#### SwitchStmtsShouldHaveDefault
1. Parse the source code and identify all switch statements.
2. For each switch statement, check whether it includes a default branch.
Example issue:
```java
switch (status) {
    case "OPEN":
        processOpen();
        break;
    case "CLOSED":
        processClosed();
        break;
}
```
A safer version includes a default branch:
```java
switch (status) {
    case "OPEN":
        processOpen();
        break;
    case "CLOSED":
        processClosed();
        break;
    default:
        handleUnknownStatus();
        break;
}
```
3. Flag the issue when a switch statement has no default case.

#### MissingBreakInSwitch
1. Parse the source code and identify all switch statements.
2. For each case, check whether execution explicitly stops before the next case.
3. A case is usually safe if it ends with one of these: break, return, throw, or continue.
Example issue:
```java
switch (status) {
    case "OPEN":
        processOpen();
    case "CLOSED":
        processClosed();
        break;
}
```

Here, case "OPEN" has no break, so execution may continue into case "CLOSED" unintentionally.

A safer version is:
```java
switch (status) {
    case "OPEN":
        processOpen();
        break;
    case "CLOSED":
        processClosed();
        break;
}
```
4. Flag the issue when a case does not end with break or another explicit exit statement.

#### AvoidInstantiatingObjectsInLoops
1. Parse the source code and identify loop structures, such as for, while, do while, enhanced for loops.
2. Inspect the body of each loop. Check whether a new object is instantiated inside the loop body.
Example issue:
```java
for (int i = 0; i < names.size(); i++) {
    StringBuilder builder = new StringBuilder();
    builder.append(names.get(i));
}
```

If the object does not need to be recreated in every iteration, move it outside the loop or reuse it when appropriate.

A possible improved version:
```java
StringBuilder builder = new StringBuilder();

for (int i = 0; i < names.size(); i++) {
    builder.append(names.get(i));
}
```
3. Flag the issue when object creation occurs repeatedly inside a loop

## Issue Tags (Additional Layer)

- Beyond PR: To compare what types of issues are most common between agent and human authors.

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| brain-overload | Code that is too complex to easily understand. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| confusing / ConfusingTernary | Code that is ambiguous or difficult to read. | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| convention | Violations of coding style and standards. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| cwe | Issues mapped to the Common Weakness Enumeration. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| design | Flaws in the structural or architectural design. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| duplicate | Redundant code segments or logic. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| suspicious | Code that likely contains logic errors. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### How to detect

#### brain-overload

1. Analyze the code structure to identify parts of the code that are difficult to understand, such as deeply nested conditions, long methods, complex branching, or complicated control flow.
2. Check whether the code violates rules related to understandability or excessive complexity.
3. If a rule detects that a method, function, or block of code is too difficult to follow, the issue can be tagged as brain-overload.

#### confusing / ConfusingTernary

1. Analyze the code for patterns that make the meaning or behaviour unclear to developers.
2. Check whether the code violates readability or clarity-related rules, such as ambiguous conditions, misleading variable or method names, confusing boolean expressions.
3. If the code does not necessarily contain a confirmed bug, but its meaning is unclear or easy to misunderstand, classify the issue as a confusing issue.

#### convention

1. Analyze the code against language-specific coding standards and style rules.
2. Check whether the code violates convention-related rules, such as inconsistent naming conventions.
3. If the issue is mainly about style, standardization, or convention, rather than a confirmed bug or vulnerability, tag it as convention.

#### cwe

1. Analyze the code for known weakness patterns that match categories in the Common Weakness Enumeration (CWE).
2. Check whether the issue is related to a recognized security weakness, such as improper input validation.
3. Determine whether the violated static-analysis rule is mapped to a CWE identifier.
4. If the rule has a CWE mapping, tag the issue as cwe.

#### design

1. Analyze the code structure to identify design decisions that may make the system harder to maintain or extend.
2. Check whether the code violates design-related rules, such as duplicated responsibilities across components or code organization that makes future changes risky.
3. If the issue is mainly about structure, architecture, or design quality, rather than a direct runtime bug or security vulnerability, tag it as design.

#### duplicate

1. Analyze the codebase to identify repeated or highly similar code segments.
2. Check whether the repeated logic appears in multiple places, such as copied blocks of code, repeated validation logic, or duplicated helper functions.
3. Determine whether the repeated code should be extracted into a shared function, helper, module, or reusable component.
4. If the issue is mainly about redundant logic or duplicated code structure, tag it as duplicate.

#### suspicious

1. Analyze the code for patterns that suggest a possible logic error or unintended behavior.
2. Check whether the code violates suspicious-logic rules, such as incorrect boolean logic, assignments used where comparisons are expected, and ignored return values that may indicate a missed error.
3. If the issue indicates that the code is likely logically wrong, even if it is syntactically valid, tag it as suspicious.


## Complexity

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Cyclomatic Complexity / Complexity | Complexity refers to Cyclomatic complexity, a quantitative metric used to calculate the number of paths through the code. Whenever the control flow of a function splits, the complexity counter gets incremented by one. Each function has a minimum complexity of 1. Strict version that counts boolean operators as decision points.<br>- Code Quality: ModifiedCyclomaticComplexity. Counts switch statements as a single decision point. | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Cognitive Complexity | How hard it is to understand the code’s control flow. Three Rules of Calculation: Ignore shorthand, Increment for breaks in linear flow, Increment for nesting. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| NPath Complexity | Measures the number of possible execution paths through a method or function. High NPath complexity indicates complex program flow. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| EmptyIfStmt | Detects an if statement with no code inside. This may indicate unfinished logic, accidentally removed code, or poor program flow. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| PrematureDeclaration | Detects variables that are declared too early before they are actually used. This can reduce readability because readers need to remember variables before they become relevant. | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

### How to detect

#### Cyclomatic Complexity / Complexity

1. Start with a base complexity of 1 for each function, because every function has at least one possible execution path.
2. Analyze the function’s control flow to find decision points where the execution path splits.
3. Increase the complexity count when the code contains structures such as if / else if conditions, loops such as for, while, or do while, case branches in switch statements, conditional expressions, logical operators that create additional decision paths, such as `&&` or `||`, exception handling branches such as catch.
4. Sum all increments within the function to get the function’s cyclomatic complexity (`CC_b`).
5. For file/repo-level analysis, combine all block-level complexity values from the analyzed files into a single unified list.
6. Calculate two summary metrics:
   - Average Cyclomatic Complexity (`CC_avg`): The mean complexity across all functions/methods/classes.
   - Maximum Cyclomatic Complexity (`CC_max`): The highest complexity value among all functions/methods/classes.
7. `CC_avg` represents the overall complexity level of the generated code, while `CC_max` identifies the single most complex function or method, which may become the main maintainability bottleneck.

#### Cognitive Complexity

1. Start from 0 for each function or method.
2. Ignore shorthand structures that make code easier to read, such as simple ternary expressions or concise syntax that does not make the logic harder to understand.
3. Add complexity when the code breaks the normal linear reading flow, such as if, else if, for, while, catch, switch/case, recursion, logical chains that are difficult to follow.
4. Add extra complexity when control-flow structures are nested inside one another. The deeper the nesting, the more difficult the code is to understand.
5. Do not only count the number of paths. Instead, evaluate how hard the logic is for a human reader to mentally follow.
6. Sum all increments to get the cognitive complexity score for the function.
7. For PR-level analysis, compare cognitive complexity before and after the PR/commit:

   `Δ cognitive complexity = cognitive_complexity_after - cognitive_complexity_before`

8. If Δ cognitive complexity > 0, the PR made the code harder to understand. If Δ cognitive complexity < 0, the PR simplified the code’s control flow.

#### NPath Complexity

1. Parse each method or function and identify all control-flow structures.
2. Count the possible execution paths created by branching structures, such as if / else, nested if statements, switch / case, loops, boolean conditions using `&&` or `||`, conditional expressions.
3. Compare with Cyclomatic complexity:
   - Cyclomatic complexity: mostly counts decision points.
   - NPath Complexity: captures methods with many nested branches or multiple independent conditions.

#### EmptyIfStmt

1. Parse the source code and identify all if statements.
2. For each if statement, check whether the body contains any executable statement.
3. If the body is empty, classify it as EmptyIfStmt, e.g.,

```java
if (condition) {
}
```
or:
```java
if (condition);
```

#### PrematureDeclaration
1. Parse the source code and identify variable declarations.
2. For each variable, find the location where it is first used.
3. Check whether the variable is declared significantly earlier than its first use.
4. If a variable is declared far before it is needed, flag it as PrematureDeclaration.

## Duplication / Reusability

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Duplications Density / DRY Violations | - AI: May regenerate similar logic in multiple files instead of reusing existing helpers.<br>- Human: More likely to reuse existing helper functions or write shorter shared utilities.<br>- Code Quality: Uses CPD/PMD code duplication issues such as Duplicate50 and Duplicate100. | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Duplicated Blocks | The number of duplicated blocks of line. | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Duplicated Lines | The number of lines involved in duplications. | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Duplicated Files | The number of files involved in duplications. | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |

### How to detect

#### Duplications Density / DRY Violations

1. Analyze the codebase to identify repeated or highly similar blocks of code across files or within the same file.
2. Check whether the repeated code represents duplicated logic, such as repeated validation logic, duplicated helper functions.
3. SonarQube detects duplicated blocks by comparing token/code sequences, not just exact text. This means duplicated logic can still be detected even if whitespace or small formatting details differ.
4. Count the number of duplicated lines detected in the codebase.
5. Calculate duplication density using:

   `Duplications Density = duplicated_lines / lines_of_code * 100`

6. If the duplication density increases after a PR/commit, it means the change introduced more repeated code or DRY violations.

#### Duplicated Blocks

1. Analyze the codebase to find repeated or highly similar sequences of code.
2. Convert the source code into comparable token/code sequences so that duplication can be detected beyond simple text matching.
3. Check whether a repeated sequence meets the minimum threshold for a duplicated block:
   - Non-Java projects: at least 100 successive duplicated tokens.
   - Java projects: at least 10 successive duplicated statements/tokens.
4. If a repeated code sequence meets the threshold, classify it as a duplicated block.

#### Duplicated Lines

1. Analyze the codebase to find code blocks that are repeated or highly similar.
2. Check whether the repeated blocks contain duplicated logic, such as copied helper functions, repeated validation logic, similar conditional branches, repeated calculations, duplicated data-processing logic, repeated error-handling structures.
3. SonarQube compares code/token sequences to detect duplication. This means it can identify duplicated blocks even when formatting or whitespace differs.
4. After duplicated blocks are detected, count the number of physical code lines that belong to those duplicated blocks.
5. The total count becomes the Duplicated Lines metric.

#### Duplicated Files

1. Analyze the codebase to identify duplicated code blocks across files or within the same file.
2. Check whether each duplicated block meets the minimum duplication threshold used by SonarQube.
3. Identify which files contain at least one duplicated block.
4. Count each file involved in duplication once, even if that file contains multiple duplicated blocks.
5. The total number of unique files containing duplicated blocks becomes the Duplicated Files metric.


## Size

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Lines of Code / ncloc | The number of physical lines that contain at least one character which is neither a whitespace nor a tabulation nor part of a comment. | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Lines | The number of physical lines, number of carriage returns. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Statements | The number of statements, e.g., `x = 5; y = 10; print(x + y)` = 3 statements. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Functions | The number of functions. Depending on the language, a function is defined as either a function, a method, or a paragraph. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Classes | The number of classes, including nested classes, interfaces, enums, and annotations. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Files | The number of files. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Comment Lines | The number of lines containing either comment or commented-out code.<br>- Pre-Post AI: discusses **high comment and documentation density** as one of the AI-generated code looks like. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Comments (%) / Comment Density | The comment lines density = comment lines / (lines of code + comment lines) * 100. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

### How to detect

#### Lines of Code / ncloc

1. Analyze each source file included in the selected language scope.
2. Read the file line by line.
3. Exclude lines that are empty or contain only whitespace/tabulation.
4. Exclude lines that contain only comments, such as full-line comments, documentation comments, block-comment-only lines.
5. Count lines that contain at least one actual code character.
6. If a line contains both code and an inline comment, count it as a line of code because it still contains executable or meaningful code.
7. Sum the counted lines across all analyzed files to obtain the total ncloc.

#### Lines

1. Read each analyzed source file line by line.
2. Count every physical line in the file.
3. A new physical line is identified by a line break/newline character, also described as a carriage return.
4. Include all types of lines in the count: code lines, comment lines, blank lines, lines containing only whitespace.
5. Sum the physical lines across all analyzed files to get the total Lines metric.

#### Statements

1. Parse the source code according to the programming language syntax.
2. Identify executable statements in the code, such as variable assignments, function or method calls, return statements, conditional statements, loop statements, object/class instantiations, expression statements.
3. Do not count blank lines or comments as statements.
4. Count each executable instruction as one statement, depending on the language-specific parser rules.
5. Sum the statements across all analyzed files to get the total Statements metric.

#### Functions

1. Parse each source file according to the programming language syntax.
2. Identify function-like declarations, such as standalone functions, class methods, object methods, constructors, language-specific procedures or paragraphs.
3. Count each detected function-like unit once.
4. Apply language-specific rules because different languages define functions differently. For example, Python uses `def`, JavaScript/TypeScript may use function declarations, arrow functions, or methods, and Java/C++ may count class methods.
5. Sum the number of functions across all analyzed files to get the total Functions metric.

#### Classes

1. Parse each source file according to the programming language syntax.
2. Identify class-like declarations, such as classes, nested classes, interfaces, enums, annotations, language-specific class/object structures.
3. Count each detected class-like structure once.
4. Apply language-specific rules because not every language defines classes in the same way. For example, Java may include classes, interfaces, enums, and annotations, while Python may count class definitions.
5. Sum the number of classes across all analyzed files to get the total Classes metric.

#### Files

1. Identify all files included in the analysis scope.
2. Exclude files that are not analyzed based on the project configuration.
3. Count each analyzed source file once.
4. Sum the number of analyzed files to get the total Files metric.

#### Comment Lines

1. Analyze each source file line by line.
2. Identify lines that contain comments based on the programming language syntax, such as `#` comment in Python, `//` comment in Java, JavaScript, TypeScript, C/C++, `/* ... */` block comments, docstrings or documentation comments depending on the language and analyzer rules.
3. Count lines that contain only comments.
4. Count lines inside multi-line or block comments.
5. Count commented-out code if it is written as a comment.
6. Do not count blank lines or whitespace-only lines as comment lines.
7. Sum all comment lines across analyzed files.

#### Comments (%) / Comment Density

1. Count the total number of comment lines.
2. Count the total number of lines of code.
3. Calculate comment density using:

   `Comment Density = comment_lines / (lines_of_code + comment_lines) * 100`


## Issues

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Blocker Issues | Number of blocker severity issues.<br>- Pre-Post AI: Discusses AI-generated code looks like patterns, but does not use severity levels. | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Critical Issues | Number of critical severity issues. | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Major Issues | Number of major severity issues. | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Minor Issues | Number of minor severity issues. | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

### How to detect

#### Blocker/Critical/Major/Minor Issues

1. Detect all issues in the analyzed code using SonarQube rules.
2. For each detected issue, check the severity level assigned by the rule.
3. Classify an issue as a Blocker/Critical/Major/Minor Issue if SonarQube assigns it the Blocker/Critical/Major/Minor severity level.
4. Blocker issues usually represent problems with very high impact, such as issues that can severely affect reliability, security, or maintainability.
5. Count the total number of issues with Blocker/Critical/Major/Minor severity.

## Coverage

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Lines to Cover | The number of lines of code that could be covered by unit tests, e.g., blank lines or full comment lines are not considered as lines to cover. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Uncovered Lines | The number of conditions that are not covered by unit tests. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Line Coverage | On a given line of code, Line coverage simply answers the question ‘Has this line of code been executed during the execution of the unit tests?’. It is the density of covered lines by unit tests. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Functional Correctness | Measures whether the generated code produces the expected outputs for the benchmark’s test cases. For each problem instance, correctness is binary: 1 if all tests pass, and 0 otherwise. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

### How to detect

#### Lines to Cover

1. Identify executable lines of code in the analyzed files.
2. Exclude lines that cannot be covered by unit tests, such as blank lines, full comment lines, whitespace-only lines, declarations or syntax elements that are not executable, depending on the language.
3. Use a test coverage report generated by the project’s testing tool to determine which lines are considered coverable.
4. Count all executable lines that could be exercised by unit tests. These become Lines to Cover.
5. Do not count whether the line was actually executed yet. Lines to Cover only measures the total number of coverable lines.

#### Uncovered Lines

1. Identify all Lines to Cover, meaning executable lines that could be covered by unit tests.
2. Import the project’s test coverage report into SonarQube, such as coverage.xml for Python, lcov.info for JavaScript/TypeScript, JaCoCo report for Java, or other language-specific coverage reports.
3. For each coverable line, check whether the coverage report marks it as executed by at least one test.
4. If a coverable line is not executed by any test, classify it as an Uncovered Line.
5. Count all coverable lines that were not executed by tests.

#### Line Coverage

1. Identify all Lines to Cover, meaning executable lines that could be covered by unit tests.
2. Import the project’s test coverage report into SonarQube.
3. For each coverable line, check whether the coverage report marks it as executed by at least one unit test.
4. Count the number of covered lines, meaning coverable lines that were executed during tests.
5. Calculate line coverage using:

   `Line Coverage = covered_lines / lines_to_cover * 100`

### Functional Correctness
1. Run the generated code using the benchmark’s official evaluation harness or test suite.
2. Check whether the code passes all required test cases.
3. If all test cases pass, assign:
    `Functional Correctness = 1`
4. If one or more test cases fail, assign:
    `Functional Correctness = 0`
5. For multiple problem instances, calculate the overall correctness rate:
    `Correctness Rate = number_of_correct_solutions / total_problem_instances * 100`

## Code Change

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Additions | Measures the number of lines added in a PR or commit. | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Deletions | Measures the number of lines deleted in a PR or commit. | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Changes / Lines Modified | Measures the total number of lines modified in a PR or commit, usually additions + deletions.<br>- Pre-Post AI: PR Size / Change Size<br><br>- Code Review Smell: Large Changesets. The changeset is too large to be reviewed. | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Elevated Code Churn | - AI: AI-authored lines are more likely to be removed, reverted, or heavily rewritten shortly after being committed.<br>- Human: Human-authored lines tend to remain more stable for longer after commit. | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Files Changed per PR | Measures the number of files modified in a PR. | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Multi-File Metric Aggregation for SWE-bench Verified | Aggregates metric differences across multiple modified files by comparing pre-patch and post-patch code. It measures the delta (Δ) between before and after versions to isolate changes caused by generated edits. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

### How to detect

#### Additions

1. Retrieve the PR or commit diff from GitHub API or Git history.
2. For each changed file, count the number of newly added lines.
3. Lines marked with `+` in the diff are counted as additions, excluding diff metadata lines such as file headers.
4. Sum all added lines across all changed files in the PR or commit:

   `Additions = sum of added lines across all changed files`

#### Deletions

1. Retrieve the PR or commit diff from GitHub API or Git history.
2. For each changed file, count the number of removed lines.
3. Lines marked with `-` in the diff are counted as deletions, excluding diff metadata lines such as file headers.
4. Sum all deleted lines across all changed files in the PR or commit:

   `Deletions = sum of deleted lines across all changed files`

#### Changes / Lines Modified

1. The number of changed LOC is calculated by summing up the number of added and deleted LOC.
2. If a changeset consists of more than 500 changed LOC, then the code review process is affected by large changesets smell.

#### Elevated Code Churn

1. Identify the lines introduced by each PR or commit.
2. Track those added lines over a fixed time window after they are committed, e.g., 7/14/30 days.
3. Check whether the introduced lines are later deleted, reverted, heavily modified, replaced by different implementation, or overwritten by later commits.
4. Count how many originally added lines did not survive within the selected time window.
5. Calculate churn rate using:

   `Code Churn Rate = removed_or_modified_added_lines / originally_added_lines * 100`

6. Compare churn rate between AI-authored and human-authored code.
7. If AI-authored lines have a higher churn rate than human-authored lines, this suggests Elevated Code Churn.

#### Files Changed per PR

1. Retrieve the PR file list from GitHub API or Git history.
2. Count each file that was modified, added, deleted, renamed, or changed in the PR.
3. Count each changed file once, even if it has multiple commits or multiple line changes within the same PR.
4. Sum the total number of changed files:

   `Files Changed per PR = count of unique files modified in the PR`

#### Multi-File Metric Aggregation for SWE-bench Verified

1. Identify all files modified by the generated patch.
2. Compute the selected metric on the pre-patch version of the modified files.
3. Apply the patch or use the post-patch version of the same files.
4. Compute the same metric again on the post-patch version.
5. Aggregate metric values across all modified files.
6. Calculate the metric difference:

   `Δ metric = metric_post - metric_pre`

7. Use the delta value to isolate the change caused by the generated edit.
8. Interpret the result based on the metric:
   - For metrics where lower is better, such as bugs, vulnerabilities, code smells, or complexity, a negative delta indicates improvement.
   - For metrics where higher is better, such as maintainability score, PyLint score, or functional correctness, a positive delta indicates improvement.

## PR Practices (Programming Behavior)

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| PR Description | - Ideal Behavior: Purpose, changes, test steps included.<br>- Non-Ideal Behavior: Empty or minimal PR description.<br><br>- Code Review Smell: Missing Context | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| PR Accepted / Merged | Measures whether a pull request was successfully merged into the target branch. | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Lack of Code Review | Measures whether a PR was merged by its own author without sufficient teammate review.<br>- Unreviewed and Self-reviewed (self-merge) | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| LGTM Reviews | The reviewer performs a lax code review and directly approves the changeset.<br>- BRIDGES: Non-constructive code reviews | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Reviewed Merge | Indicates whether a PR was merged after being reviewed by teammates. | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Number of Reviews | Measures the number of reviews submitted on a PR. | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Sleeping Reviews (Time to Close/Merge) | The process takes too long in terms of time. Measures the time between PR creation and PR close or merge (Time to Close/Merge). This metric captures how long a PR remains open before it is accepted, rejected, or closed. | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| PR Task Type | Classifies the type of PR task, such as feat, test, or docs, and can be used as a predictor of PR acceptance. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### How to detect

#### PR Description

1. The text pattern to link the related issues of reviews in each project is achieved by analyzing the related guidelines.
2. Heading and changeset description of each review instance are mined in order to check whether they include a related issue number/ID or a proper explanation of the changeset. If the PR author leaves the description field empty or copies the PR title and pastes it into the PR description field, then it is missing a proper description.
3. If a review process is not linked to a related issue and a proper description of the changeset is not provided, then it is affected by the smell: missing context in reviews.
4. A PR is affected by the smell missing context in reviews if its body field is the same as the heading field or does not include any further description/linked issue information.

#### PR Accepted / Merged

1. Retrieve PR metadata from GitHub API or Git history.
2. Check whether the PR has a non-null `merged_at` timestamp.
3. If `merged_at` exists, classify the PR as accepted / merged.
4. If `merged_at` is empty or null, check the PR state:
   - closed but not merged = rejected / closed unmerged,
   - open = still pending,
   - merged = accepted.
5. Store the PR acceptance value as a binary variable:
   - PR Accepted = 1 if `merged_at` is not null
   - PR Accepted = 0 if closed without merge
6. For merge rate analysis, calculate:

   `Merge Rate = number_of_merged_PRs / total_number_of_closed_PRs * 100`

7. For author-group comparison, compare merge rates between groups, such as AI-agent vs human-authored PRs or pre-GenAI vs post-GenAI repositories.

#### Lack of Code Review

1. If the changeset is merged to the project codebase without a code review, then it is an unreviewed commit.
2. If the one and only reviewer of a changeset is the author of it, then it is a self-reviewed commit.
3. If a review consists of unreviewed or self-reviewed changesets, then it is affected by the smell: lack of code review.

#### LGTM Reviews

1. Retrieve review comments and approval events from the PR using GitHub API or code review history.
2. Check whether the reviewer approved the PR or changeset.
3. Analyze the review text/comment body.
4. If the review comment is empty, very short, or only contains generic approval phrases, classify it as an LGTM review, e.g., LGTM, Looks good to me, approved, good, nice, +1, ship it.
5. Check whether the review contains meaningful feedback, such as pointing out a defect, suggesting an improvement, asking for clarification, mentioning testing, discussing design, readability, or maintainability.
6. If the review approves the PR but does not include meaningful feedback, classify the review process as affected by the LGTM Reviews smell.

#### Reviewed Merge

1. Retrieve PR metadata from GitHub API, including PR author, reviewers, review events, approval events, merge status, merge actor.
2. Check whether the PR was merged by verifying that `merged_at` is not null.
3. Identify whether at least one teammate or reviewer other than the PR author reviewed or approved the PR before it was merged.
4. Exclude self-approval or self-review from the reviewed-merge count.
5. If the PR was merged after receiving at least one valid review or approval from someone other than the author, classify it as a Reviewed Merge.
6. If the PR was merged without any valid teammate review, classify it as Self-Merge or No Review Merge.
7. For PR-level analysis, calculate:
   - Reviewed Merge = 1 if `merged_at` is not null and valid_teammate_review_exists
   - Reviewed Merge = 0 otherwise
8. For repository-level analysis, calculate:

   `Reviewed Merge Rate = reviewed_merged_PRs / total_merged_PRs * 100`

#### Number of Reviews

1. Retrieve PR review data from GitHub API or the project’s code review platform.
2. For each PR, count submitted review events, such as approval reviews, change request reviews, comment-only reviews.
3. Optionally exclude reviews submitted by the PR author if the goal is to measure peer review only.
4. Optionally count unique reviewers separately if the goal is to measure reviewer diversity.
5. Store the total number of reviews for each PR:

   `Number of Reviews = count of submitted review events on the PR`

#### Sleeping Reviews (Time to Close/Merge)

1. The elapsed time between the creation and completion moments of each code review process is calculated and named review sleeping time (`RSTime`).

   `RSTime = t_reviewCompleted - t_reviewCreate`

2. Set the threshold for a sleeping review as 48 h.
3. Sleeping review occurs when the code review takes more than two days.

#### PR Task Type

1. Retrieve PR metadata from GitHub API, including PR title, PR body/description, branch name, commit messages, PR labels, linked issue labels if available.
2. Search for task-type keywords or conventional commit prefixes, such as:
   - feat / feature = new feature,
   - fix / bugfix = bug fix,
   - docs = documentation change,
   - test = test-related change,
   - refactor = code restructuring without changing behavior,
   - chore = maintenance/configuration task,
   - style = formatting/style change,
   - ci = CI/CD configuration.
3. Prioritize explicit labels or conventional commit prefixes when available, e.g.,
   - feat: add login page,
   - fix: resolve API timeout,
   - docs: update README,
   - test: add unit tests.
4. If no explicit prefix exists, infer the task type from the PR title, description, file paths, or changed files, e.g.,
   - changes only in `README.md` or `/docs` → docs,
   - changes mainly in `/tests` or `test_*.py` → test,
   - changes in GitHub Actions or CI config → ci,
   - code restructuring without new feature language → refactor.
5. Assign one primary task type per PR. If multiple categories apply, use a priority rule or allow multi-label classification depending on the study design.
6. For PR acceptance analysis, use task type as a categorical predictor:

   `PR Task Type ∈ {feat, fix, docs, test, refactor, chore, style, ci, other}`


## Branching (Programming Behavior)

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Branch Naming | - Ideal Behavior: Descriptive and Meaningful Branch Name, e.g., feat, login.<br>- Non-Ideal Behavior: Random Branch Name/Generic Names, e.g., developer’s own name, bug, test, new.<br>- Code Review Smell: Missing context | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Branching Strategy | - Ideal Behavior: One Feature Per Branch.<br>- Non-Ideal Behavior: Multiple Features Per Branch. | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |

### How to detect

#### Branch Naming

1. Retrieve the branch name for each PR from GitHub API or Git history.
2. Normalize the branch name by converting it to lowercase and removing separators such as `/`, `_`, or `-` when needed.
3. Check whether the branch name contains meaningful task-related information, such as feature name, bug/fix description, issue number, module/component name, task type prefix such as `feat/`, `fix/`, `docs/`, `test/`, or `refactor/`.
4. Classify the branch as meaningful if it clearly describes the purpose of the work, e.g., `feat/login-page`, `fix/payment-timeout`, `docs/update-readme`, `refactor/user-service`, `issue-123-profile-api`.
5. Classify the branch as random/generic if it does not clearly explain the work, e.g., `test`, `bug`, `new`, `update`, `final`, developer’s own name only, random letters/numbers with no issue reference.
6. Encode the result as:

   `Branch Naming = meaningful or random/generic`

#### Branching Strategy

1. Retrieve the PR branch name, PR title, PR description, linked issue, commit messages, and changed files from GitHub API or Git history.
2. Check whether the branch/PR is focused on one clear task, feature, bug fix, documentation update, or refactor.
3. Classify the branch as one feature per branch if:
   - the branch name points to one task or issue,
   - the PR description explains one main purpose,
   - commits are related to the same feature/fix,
   - changed files support one coherent change.
4. Classify the branch as multiple features per branch if:
   - the PR includes unrelated features or fixes,
   - commit messages mention different tasks,
   - changed files touch unrelated modules,
   - the PR description lists several independent changes,
   - the branch combines feature work, refactoring, testing, and documentation that are not directly tied to the same task.
5. Encode the result as:

   `Branching Strategy = one_feature or multiple_features`


## Code Structure

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Feature/Refactor Code Size | - Ideal Behavior: Small Feature/Small code commits or Small Refactor/Incremental refactor commits.<br>- Non-Ideal Behavior: Large Feature/Large code commits or Large Refactors.<br>- Code review smell: Large Changesets | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Keep repository up-to-date | - Ideal Behavior: Pulling latest changes.<br>- Non-Ideal Behavior: Ignoring merge conflicts. | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Code integration | - Ideal Behavior: All changes are linked to a PR.<br><br>- Non-Ideal Behavior: Changes are pushed directly to the main branch without association to a PR (orphan commits). | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

### How to detect

#### Feature/Refactor Code Size

1. Retrieve PR or commit metadata from GitHub API or Git history, including changed files, additions, deletions, commit messages, PR title and description.
2. Identify whether the change is a feature change. This can be inferred from:
   - PR title or branch prefix such as `feat/` or `feature/` or `refactor/`,
   - commit message prefix such as `feat:` or `refactor:`,
   - PR labels such as feature or refactor,
   - description indicating new functionality or code restructuring without intended behaviour change.
3. Calculate the size of the feature change:

   `Feature/Refactor Code Size = additions + deletions`

4. Classify the feature/refactor as small if the changed LOC is below the selected threshold.
5. Classify the feature/refactor as large if the changed LOC exceeds the selected threshold.
6. In BRIDGES detection, a common rule is:

   `Small Feature/Refactor = changed LOC < 50`

   `Large Feature/Refactor = changed LOC ≥ 50`

7. For code review smell detection, if the feature change/refactor is very large, for example more than 500 changed LOC, it may also be affected by the Large Changesets smell.

#### Keep repository up-to-date

1. Retrieve the PR branch and target/base branch information from GitHub API or Git history.
2. Compare the PR branch with the latest version of the base branch, such as main, master, or develop.
3. Check whether the PR branch is behind the base branch.
4. Check whether the PR has merge conflicts or cannot be merged cleanly.
5. Classify the PR branch as up-to-date if:
   - it includes the latest relevant changes from the base branch,
   - it can be merged cleanly,
   - and there are no unresolved merge conflicts.
6. Classify the PR branch as outdated if:
   - it is behind the base branch,
   - it has unresolved merge conflicts,
   - or it has not been updated after new commits were added to the base branch.
7. Encode the result as:

   `Repository Status = up-to-date or outdated`

#### Code integration

1. Retrieve all commits from the repository’s main branch, such as main, master, or develop.
2. Retrieve all PRs and their associated commits using GitHub API or Git history.
3. For each commit on the main branch, check whether the commit is linked to a PR.
4. A commit is considered properly integrated if:
   - it appears in a merged PR,
   - it is associated with a PR number,
   - or it is part of a merge/squash/rebase commit connected to a PR.
5. A commit is considered an orphan commit if:
   - it appears directly on the main branch,
   - it is not linked to any PR,
   - and it bypasses the normal PR review process.

## Coding Style / AI-Generated Looks Like

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Verbose, Descriptive Identifier Naming | - AI: Long, self-explanatory, and full descriptive identifiers within function bodies: temporary variables, loop counters, and intermediate results.<br>- Human: Names get shortened, abbreviated, and use different naming styles in different files. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| High Comment and Documentation Density | - AI: AI-generated functions tend to come with a docstring with one-line summary, an Args block, a Returns block, and sometimes a Raises block. Inline comments restate what the next line does in slightly more verbose language.<br>- Human: Comments are sparse, sometimes outdated, and clustered around the parts the author actually found tricky rather than spread evenly across all functions. Tend to encode context that lives nowhere else in the code: ticket numbers, references to deprecated APIs, a quick note on why the obvious approach was skipped. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Consistent Whitespace and Indentation | - AI: Produces highly consistent indentation, blank-line spacing, and spacing around operators, often resembling code that has been formatted by a linter.<br>- Human: Formatting may drift across files or functions, such as inconsistent blank lines, spacing, or indentation styles that are still tolerated by linters. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Hyper-consistent Error Handling | - AI: Often wraps functions in highly structured try/except blocks, catches multiple specific exceptions, logs each error with formatted messages, and re-raises them even when not needed.<br>- Human: Error handling is usually less uniform and more context-dependent, with some functions catching no exceptions and others catching only relevant errors. | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### How to detect

#### Verbose, Descriptive Identifier Naming

1. Extract identifier names from the source code, including function names, method names, variable names, loop counters, temporary variables, class names, and intermediate result variables.
2. Calculate identifier-level features, such as average identifier length, median identifier length, number of words/tokens per identifier, percentage of long identifiers, percentage of abbreviated identifiers, and consistency of naming style across files.
3. Use the following threshold to classify a long descriptive identifier:
   - Identifier length ≥ 20 characters, or
   - Identifier contains ≥ 3 meaningful word tokens.

   For example:
   - `number_of_successful_transactions` → verbose/descriptive
   - `calculateAverageTransactionValue` → verbose/descriptive
   - `temporary_user_profile_response` → verbose/descriptive
4. Classify identifiers as short/abbreviated if they use shortened or compact names, e.g., `avg_txn`, `tmp`, `usr`, `i`, `res`.
5. Use the following threshold to classify abbreviated identifiers:
   - Identifier length ≤ 5 characters
6. Calculate a score such as:

   `Verbose Identifier Rate = long_descriptive_identifiers / total_identifiers * 100`

7. Classify the code as showing verbose/descriptive identifier naming if:

   `Verbose Identifier Rate ≥ 30%`

8. If the verbose identifier rate is high across many files, the code may show an AI-like naming pattern.

#### High Comment and Documentation Density

1. Extract comments and documentation text from the source code, including docstrings, block comments, inline comments, function/method documentation, and class documentation.
2. Identify structured documentation patterns commonly associated with AI-generated code, such as one-line summary, Args: / Parameters: section, Returns: section, Raises: section, and highly consistent documentation format across many functions.
3. Measure comment/documentation density using features such as number of comment lines, comment-to-code ratio, percentage of functions with docstrings, average docstring length, and percentage of functions with structured sections like Args, Returns, or Raises.
4. Check whether inline comments simply restate the next line of code instead of adding useful context.
5. Classify the code as showing high comment and documentation density if it has many structured docstrings, repeated documentation templates, high comment-to-code ratio, and redundant inline comments.
6. Calculate a score such as:

   `Comment Density = comment_lines / (lines_of_code + comment_lines) * 100`

7. If the comment density or structured documentation rate is unusually high, the code may show an AI-like documentation pattern.

#### Consistent Whitespace and Indentation

1. Extract formatting features from source files, such as indentation depth, spaces vs tabs, blank-line frequency, spacing around operators, spacing after commas, line breaks between functions/classes, and consistency of formatting across files.
2. Measure how consistent these formatting patterns are within each file and across the repository.
3. Check whether the code follows highly uniform formatting patterns, such as same indentation width everywhere, consistent blank lines between functions, consistent spacing around operators, consistent line wrapping, and formatting that closely resembles linter output.
4. Compare this consistency against more human-like formatting, where small variations may appear across files or functions.
5. Compute a formatting consistency score:

   `Formatting Consistency Score = consistently_formatted_lines / total_lines * 100`

6. If formatting consistency is unusually high across many files/functions, the code may show an AI-like pattern.

#### Hyper-consistent Error Handling

1. Extract exception-handling structures from the code, such as:
   - `try/except` in Python,
   - `try/catch` in Java, JavaScript, TypeScript, C++, or similar languages.
2. Identify whether many functions use a repeated error-handling template, such as wrapping the whole function body in `try/except`, catching several specific exception types in sequence, logging every exception with similarly formatted messages, re-raising the exception after logging, or adding broad fallback handlers such as `except Exception`.
3. Check whether the error handling is contextually necessary. For example, if a function catches many exceptions even though the caller should handle them, this may indicate overly defensive or templated error handling.
4. Measure consistency across functions/files, such as percentage of functions with try/except blocks, average number of exception handlers per function, percentage of handlers that log and re-raise, repeated similarity of error messages, and frequency of broad exception catches.
5. Classify the code as showing hyper-consistent error handling if many functions use similar, structured, repetitive exception-handling patterns regardless of context.


## AI Detection

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Binoculars | Uses two related LLMs, an observer and a performer, to score whether code looks AI-generated. If the two models strongly agree on what tokens are likely to come next, the code is treated as more AI-like. If the observer is more surprised while the performer is not, the code is treated as more human-like. | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| File-level AI Density | Measures the proportion of files in a repository that are classified as AI-like. | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Team Prediction | Predicts whether a team’s code is more AI-like or human-like using Binoculars. Team-level scores are aggregated from code chunks/files to classify the team. | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Agent Type / Name | Identifies which AI agent authored/submitted the PR, such as Claude Code, Copilot, Cursor, Devin, or OpenAI Codex. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AI vs Human PR Attribution | Identifies whether a PR is authored by an AI agent or a human developer using the AIDev dataset. | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### How to detect

#### Binoculars

1. Collect the code text to be evaluated, such as a file, function, commit diff, or repository sample.
2. Pass the same code text into two related language models:
   - Observer model: measures how surprising or predictable the code is.
   - Performer model: provides a comparison signal using a related but different model.
3. Calculate the perplexity of the observer model. Perplexity measures how surprised the model is by the next tokens in the code.
4. Calculate the cross-perplexity between the observer and performer models. This compares how similarly the two models predict the code.
5. Compute a Binoculars-style score using the relationship between observer perplexity and cross-perplexity.
6. Interpret the score:
   - If the two models strongly agree and the code is highly predictable, the code is more likely to be AI-like.
   - If the observer is more surprised while the performer is not, the code is more likely to be human-like.
7. Apply a threshold to classify the code as AI-like or human-like.
8. Calculate an AI-likeness score per file.

#### File-level AI Density

1. Collect all source code files from the repository.
2. Exclude files that should not be analyzed, such as generated files, dependency/vendor files, and build artifacts.
3. Run an AI-code detector, such as Binoculars, on each eligible file.
4. Assign each file an AI-likeness score.
5. Apply a classification threshold to label each file as either AI-like or human-like.
6. Count the number of files classified as AI-like.
7. Calculate file-level AI density:

   `File-level AI Density = AI-like files / total analyzed files * 100`

#### Team Prediction

Compare File-level AI Density percentage across repositories or teams.

#### Agent Type / Name

1. Retrieve PR metadata from GitHub API or the selected dataset.
2. Check whether the PR author or committer is associated with a known AI agent account, bot, or tool.
3. If using an existing labeled dataset, such as AIDev, use the dataset’s author/agent label directly.
4. If no labeled dataset is available, infer agent type from metadata signals, such as bot account username, committed-by or co-authored-by fields, PR text mentioning the AI agent, GitHub App identity, commit signature, or automation marker.
5. Assign one agent label per PR when possible:

   `Agent Type ∈ {Claude Code, Copilot, Cursor, Devin, OpenAI Codex, Human, Unknown}`

6. If the PR is not associated with any known AI agent, classify it as Human or Unknown.

#### AI vs Human PR Attribution

1. Retrieve PR records from the selected dataset or GitHub API.
2. Match each PR to an authorship label from the AIDev dataset.
3. Check whether the PR author is identified as AI agent or human developer.
4. If the PR is linked to a known AI coding agent, classify it as AI-authored.
5. If the PR is submitted by a human developer account and not associated with an AI agent label, classify it as human-authored.
6. Store the attribution as a binary or categorical variable:

   `Author Type = AI Agent or Human`

7. Use this label to compare metrics across groups, e.g.,
   - Average Δ code quality metric for AI-authored PRs.
   - Average Δ code quality metric for human-authored PRs.


## Balanced Work

| Metric | Definition | Beyond PR | Pre-Post AI | BRIDGES | Code Review Smells | Code Quality | Metrics Paper | SonarQube |
|---|---|---|---|---|---|---|---|---|
| Review Buddies / Proactive Code Reviews | The author assigns the same reviewer(s).<br>- Ideal Behavior: Different members serve as first and second reviewers at different times.<br>- Non-Ideal Behavior: Certain individuals consistently serve as the first or the second reviewer. | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Ping-pong | Excessively long loops between author and reviewer. When the reviewer requests the author to make some additional changes on the code changeset, the author is supposed to update their changeset by considering the requests of the reviewer. The loop between the author and reviewer continues until the reviewer is satisfied with the changeset and approves that it is ready to be merged to the codebase. | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |

### How to detect

#### Review Buddies / Proactive Code Reviews

1. Self-reviewed and unreviewed commits are eliminated.
2. Commits authored by a developer having fewer than 50 contributions are ignored in order to obtain the core developers of each project. This threshold is applied in order to avoid the situation that when a developer has a small number of contributions, the reviewers assigned for these commits become the review buddies of this developer artificially.
3. All `(Author, Reviewer)` pairs and their corresponding numbers of occurrence are listed for each core author.
4. If there exists a reviewer who reviewed at least half of the commits submitted by an author, then this reviewer is called the review buddy of the author.

#### Ping-pong

1. If a review process consists of an excessively large number of iterations between the author and reviewer, it is affected by the smell: reviewer-author ping-pong.
2. This loop should not exceed three iterations.
3. If a review process consists of more than three iterations between the author and reviewer, then it is affected by the smell: reviewer-author ping-pong.