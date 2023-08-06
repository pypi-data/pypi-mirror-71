<p align="center">
  <img src="https://raw.githubusercontent.com/mateuszz0000/repofinder/master/assets/logo_v01.png">
</p>
<p align="center">
   <a href="https://travis-ci.com/github/mateuszz0000/repofinder">
        <img src="https://travis-ci.com/mateuszz0000/repofinder.svg?branch=master">
    </a>
    <a href="https://codecov.io/gh/mateuszz0000/repofinder">
        <img src="https://img.shields.io/codecov/c/github/mateuszz0000/repofinder">
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
    </a>
</p>

## What is repofinder?
Repofinder is a simple Python tool for automatic search projects with good first issues you could contribute!

## How to install this tool?
You have several choices which way you want to install repofinder:
1) via pip: `pip install repofinder` 
2) from source:
```bash
git clone https://github.com/mateuszz0000/repofinder
pip install repofinder
```
3) you can use it without installation. Just clone it and call `python main.py`

## How to use it?`
Just create `<YOUR_FAOUVIRITE_NAME>.yml` file based on following structure:
```yaml
language: <NAME>

created:
  gt: <DATE>
  lt: <DATE>

pushed:
  gt: <DATE>
  lt: <DATE>

stars:
  gt: <NUMBER>
  lt: <NUMBER>

forks:
  gt: <NUMBER>
  lt: <NUMBER>
```
and call `python main.py --params <PATH_TO_YOUR_YML_FILE>` and wait for output.

## Example
<h1 align="center">
  <img src="https://raw.githubusercontent.com/mateuszz0000/repofinder/master/assets/example_1.png">
</h1>

## Contribution
This project is in very beginning stage and there a lot to do so any contributions are welcome!
