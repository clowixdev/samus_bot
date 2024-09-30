# Samus rush royale Telegram bot

## About

**Rush Royale Clan Helper (RRCH bot &#129302;)** is created to help clan leaders and officers in communication with clan members. Using this bot, you can create **message templates&#128211;** and send them as you need to all clan members. Also, you can **mention &#128226;** everyone in your Telegram chat with only one command, or you can mention specific player **groups &#128101;** (who can clear fraction fields in **Dragon Event &#128009;**). All this information is stored in clan member's **profile &#129706;** where you can find any desired information. All clan members have to authenticate through **secret word &#128272;**, that will be known only by clan admins, so no one can enter this bot accidentally.

## Installation

To launch project locally, you need to prepare environment for the project, i'm using `pyenv`

```console
pyenv install 3.10.15
cd </project/folder>
pyenv local 3.10.15
pyenv exec python -m venv .venv
source .venv/bin/activate(.fish) # if you using fish console
pip install -r requirements.txt
python app.py
```

## What to change in code for every new clan

1. Telegram bot token
2. Telegram leader id's
3. Requirements for appliance
4. Clan name in `tokens.env`
5. `msg_templates.py` - delete names and @-tags
6. Clan chat link

## Fixes to do:

    1. Work out correct behavior while deleting templates - DONE
    2. Fix behavior while generating empty templates - DONE
    3. If user is not a member, ask him to auth or drop dialogue - DONE
    4. Show different keyboards for admin users and not-admin users - DONE
    5. Check pictures amount - DONE
    6. work with local ids when deleting and choosing templates - DONE
    7. Create a spam defend decorator - DONE
    8. register check when entering platform - DONE
    10. telegram api error about runtime fix - DONE
    11. fix no @username users - DONE
    12. try/except around send_message in case bot is blocked - DONE
    13. try/except around send_media_group in case caption is too long - DONE

## TODO:

    1. Add inline keyboards - DONE
    2. Add "/view" command to view added templates (show only first 20 symbols of generated template) - DONE
    3. Add player "profile" that will be filled during registration (fractions, crit dmg) - DONE
    4. Add mentioning based on fraction - DONE
    5. Add "description" to template while creating to show it instead of full template - DONE
    6. Add picture handling that is sent with text when creating template or sending message immediately - DONE
    7. Add group_chat keyboard (consist only fraction and everyone mentions) - DONE
    8. Add pawns mention (banshee, tesla, robot, panda) - DONE
    9. Add ability to edit profile - DONE
    10. Add "Hello" message when someone is entering main chat - DONE 
    11. Change everything "Samus Helper" to "RRClan Helper" - IN PROCESS
    12. Add base commands for Dev-only (reboot, stats, adduser)
    13. Add /bug command, that will ease bug-report process
    14. Add strategies for different modifiers
    15. Add some info about items, pawns and etc...
