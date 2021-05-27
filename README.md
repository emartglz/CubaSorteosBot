# DandoYDandoBot

## Release

To create a new release, run

```
git checkout master  # you have to place tags on master branch
git tag v<new-version>
git push --tag  # this will run the github workflow and create a new docker image
```

## How to use

Create a GITHUB_TOKEN with the pull package authorization and save it into the file `GITHUB_TOKEN.txt`

```
cat ./GITHUB_TOKEN.txt | docker login https://docker.pkg.github.com -u <GITHUB_USER> --password-stdin
```

then you can run this using

```
docker run --rm docker.pkg.github.com/kikexd/cubasorteosbot/image:latest
```
