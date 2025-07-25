from os import path as ospath, environ
from subprocess import run as srun
from requests import get as rget
from dotenv import load_dotenv
from config import logger
CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL')
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            logger.error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        logger.error(f"CONFIG_FILE_URL: {e}")
except:
    pass

load_dotenv('config.env', override=True)

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = "https://github.com/jaungimein/TgSearchBot"

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', '')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'main'

if ospath.exists('.git'):
    srun(["rm", "-rf", ".git"])

update = srun([f"git init -q \
                 && git config --global user.email desmondmile166@gmail.com \
                 && git config --global user.name Johnmclane5 \
                 && git add . \
                 && git commit -sm update -q \
                 && git remote add origin {UPSTREAM_REPO} \
                 && git fetch origin -q \
                 && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

if update.returncode == 0:
    logger.info('Successfully updated with latest commit from UPSTREAM_REPO')
else:
    logger.error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')
