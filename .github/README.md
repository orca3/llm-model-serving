# Code Release 101 

The release verison in this repo follows the [Semantic Versioning 2.0.0](https://semver.org/) - **MAJOR.MINOR.PATCH**. Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

## The Automated Release Pipeline 

### Overview
The automated pipeline in this repo will:
1. Create a new release PR (or update the existing release PR) and update [CHANGELOG.md](https://github.com/orca3/llm-model-serving/blob/main/CHANGELOG.md) when it detects a github commit pushed to the `main` branch. 
    - The new release PR is created automatically by the pipeline, and the release version (in the PR) dependeds on the messages of the pending released commits. 
    
        >For example, the prefix text 'fix' (in a commit message) increases the Patch version, 'feat' increases the Minor version and 'feat!:' or 'fix!:' or 'refactor!' increases the Major version.
    - Once the release PR is merged, a new release & a new github tag will be published in a few minutes.
    - Look into more details at the ['code-release'](https://github.com/orca3/llm-model-serving/blob/main/.github/workflows/code-release.yml) pipeline
2. Publish docker image from the `images` folder to Docker Hub [orca3ai](https://hub.docker.com/repositories/orca3ai) repository.
    - When a `new commit` is pushed to main branch, Docker image will be built and pushed with tags "main" and "commit hash" (such as [sha-6cb7ab5](https://hub.docker.com/layers/orca3ai/demo-image/sha-6cb7ab5/images/sha256-ac11ab2aa9e5cd6a8e5851a6d4dc13a18b6cc50d0bf11e4c25edad53efce3ec0?context=explore)). 
    - When a `new release` is pushed or a `new tag` is created, Docker image will be labled with tags `release version` (such as [0.1.2](https://hub.docker.com/layers/orca3ai/demo-image/0.1.2/images/sha256-ac11ab2aa9e5cd6a8e5851a6d4dc13a18b6cc50d0bf11e4c25edad53efce3ec0?context=explore)) and `latest`.


### How should I write my commits to leverage the release pipeline?

In order to leverage the automated release process mentioned above, we adopt the [Conventional Commit messages](https://www.conventionalcommits.org/en/v1.0.0/) in this repository.

**The most important prefixes you should have in mind are:**

* `fix`: which represents bug fixes, and correlates to a SemVer patch.
* `feat`: which represents a new feature, and correlates to a SemVer minor.
* `feat!`:, or `fix!`:, `refactor!`:, etc., which represent a breaking change (indicated by the !) and will result in a SemVer major.

Types other than fix: and feat: are allowed, for example [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) (based on the Angular convention) recommends `build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others`.

Read more in: [Specification](https://www.conventionalcommits.org/en/v1.0.0/#specification) and [Examples](https://www.conventionalcommits.org/en/v1.0.0/#examples).

### The Release and Docker Image Publish Process

Code release and docker image publish are fully automated in the repo, we only need to review the auto generated release PR and merge it to start the process. For example [chore(main): release 0.1.2](https://github.com/orca3/llm-model-serving/pull/16). 

Once we merge the PR, the pipeline will create git release and tag, it will also publish images to Docker Hub [orca3ai] registry. 

Every commit in main branch results a new docker build and publish. The tags are "main" and "commit hash". The release pipeline will:
* create a release PR if there is no existing release PR. 
* append the commit to the current release PR. For example [chore(main): release 0.1.2](https://github.com/orca3/llm-model-serving/pull/16)

**To start the release and docker publish process**

We need to merge the release PR, which kicks off the git release & tag creation and official docker image publish (tags with version and "latest") process.


### Test release pipeline
Besides making real commit, you can use `git commit --allow-empty -m "{message}"` to test different reaction of the release pipeline. 

For example:

* Set the release number to a specific version: 'git commit --allow-empty -m "chore: release 2.0.0" -m "Release-As: 2.0.0"', the pipeline will set the release version to 2.2.0. 
* Bump up the PATCH version: 'git commit --allow-empty -m "fix: fix a small issue in the flask docker image" '



## References:

### GitHub Actions
* [GitHub Actions documentation](https://docs.github.com/en/actions)
* [GitHub Actions: Publishing Docker images](https://docs.github.com/en/actions)
* [GitHub Action: Metadata Action](https://github.com/docker/metadata-action?tab=readme-ov-file#about)
* [GitHub Actions: Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

### Release-please Action
* [Google Release-Please Official Site & User Guide](https://github.com/marketplace/actions/release-please-action#release-types-supported)
* [GitHub link with more examples](https://github.com/googleapis/release-please)