import subprocess
import os
import shutil
from dotenv import load_dotenv

load_dotenv(override=True)

BUILD_DIR = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/sonarqube_dependencies/builds/project-4-direct-geo-referencing"
LIB_PATH = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/sonarqube_dependencies/libs"

EXCLUSIONS = ("Front-end/src/app/map/map.component.ts,**/leaflet/**,**/.git/**,**/.github/**,**/.idea/**,"
              "**/.vscode/**,**/.scannerwork/**,**/.sonar/**,**/.cache/**,**/__pycache__/**,**/node_modules/**,"
              "**/bower_components/**,**/vendor/**,**/vendors/**,**/bin/**,**/obj/**,**/build/**,**/dist/**,"
              "**/target/**,**/out/**,**/coverage/**,**/.gradle/**,**/.next/**,**/.nuxt/**,**/.venv/**,**/venv/**,"
              "**/.dart_tool/**,**/Pods/**,**/DerivedData/**,**/.terraform/**,**/test/**,**/tests/**,**/__tests__/**,"
              "**/spec/**,**/e2e/**,**/PHPTest/**,**/mocks/**,**/mock/**,**/fixtures/**,**/*Test.*,**/*Tests.*,"
              "**/*.spec.*,**/*.test.*,**/*_test.php,**/*.po.*,**/test.ts,**/*.png,**/*.jpg,**/*.jpeg,**/*.gif,"
              "**/*.svg,**/*.pdf,**/*.zip,**/*.7z,**/*.rar,**/*.tar,**/*.gz,**/*.class,**/*.md,**/*.txt,**/*.csv,"
              "**/*.json,**/*.yml,**/*.yaml,**/*.xml,**/*.properties,**/*.lock,**/*.log,**/*.tmp,**/*.ico,"
              "**/*.exe,**/*.dll,**/*.so,**/*.dylib,**/*.doc,**/*.docx,**/*.ppt,**/*.pptx,**/*.xls,**/*.xlsx,"
              "**/*.mdb,**/*.jar,**/*.mp3,**/*.mp4,**/*.aar,**/*.bat,**/*.sh,**/*.example,**/*.template,"
              "**/*.prisma,**/*.graphql,**/*.config,**/*.psd,**/*.bak,**/*.asta,**/*.tex,**/*.d.ts,**/*.js.map,"
              "**/*.conf.js")

def run_command(command, cwd=None):
    process = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"Error output: {process.stderr}")
        raise Exception(f"Command failed with return code {process.returncode}")
    print(process.stdout)

def find_jars():
    if not os.path.exists(LIB_PATH):
        return ""
    jars = [os.path.join(LIB_PATH, f) for f in os.listdir(LIB_PATH) if f.endswith(".jar")]
    return os.pathsep.join(jars)

def main():

    target_dir = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/clone_repo/UBCO-COSC499-Winter-2018-Term-1-2/project-4-direct-geo-referencing"

    java_files = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))

    sonar_cmd = [
        "sonar-scanner",
        f"-Dsonar.projectKey={os.getenv('SONAR_PROJECT_KEY')}",
        f"-Dsonar.projectName={os.getenv('SONAR_PROJECT_NAME')}",
        "-Dsonar.sources=.",
        "-Dsonar.sourceEncoding=UTF-8",
        f"-Dsonar.host.url={os.getenv('SONAR_HOST_URL')}",
        f"-Dsonar.token={os.getenv('SONAR_TOKEN')}",
        f"-Dsonar.exclusions={EXCLUSIONS}"
    ]

    if len(java_files) > 0:
        print(f"Java project detected ({len(java_files)} files). Preparing compilation...")
        classpath = find_jars()

        if os.path.exists(BUILD_DIR):
            shutil.rmtree(BUILD_DIR)
        os.makedirs(BUILD_DIR, exist_ok=True)

        javac_cmd = ["javac", "-d", BUILD_DIR]
        if classpath:
            javac_cmd += ["-cp", classpath]
        javac_cmd += java_files

        run_command(javac_cmd, cwd=target_dir)
        sonar_cmd.append(f'-Dsonar.java.binaries="{BUILD_DIR}"')
    else:
        print("No Java files detected. Continuing scan as a non-Java project...")

    run_command(sonar_cmd, cwd=target_dir)

if __name__ == "__main__":
    main()

# Run: python -m src.sonarqube.run_sonar_scanner