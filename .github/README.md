# Repository Release 101 

## The Automated CI Pipeline
In this repo, describe release, version and docker image publish




### How should I write my commits?

In order to leverage the automated release process () using [Conventional Commit messages](https://www.conventionalcommits.org/en/v1.0.0/).

**The most important prefixes you should have in mind are:**

* `fix`: which represents bug fixes, and correlates to a SemVer patch.
* `feat`: which represents a new feature, and correlates to a SemVer minor.
* `feat!`:, or `fix!`:, `refactor!`:, etc., which represent a breaking change (indicated by the !) and will result in a SemVer major.

Types other than fix: and feat: are allowed, for example [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) (based on the Angular convention) recommends `build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others`.

Read more at: [Specification](https://www.conventionalcommits.org/en/v1.0.0/#specification) and [Examples](https://www.conventionalcommits.org/en/v1.0.0/#examples)

### When to publish release


## References:

### GitHub Actions
* [GitHub Actions documentation](https://docs.github.com/en/actions)
* [GitHub Actions: Publishing Docker images](https://docs.github.com/en/actions)
* [GitHub Actions: Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
