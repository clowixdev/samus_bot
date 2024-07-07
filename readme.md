# Samus rush royale Telegram bot

This telegram bot will be used as notifier for clan members. Also, this bot can be used as mentioner and informator. You can check strategies and decks for different modifiers and get other useful information. All clan members have to authenticate through secret word, that will be known only by devs, so no one can enter this bot. 

## Fixes to do:
    1. Work out correct behavior while deleting templates - DONE
    2. Fix behaviour while generating empty templates - DONE
    3. If user is not a member, ask him to auth or drop dialogue - DONE
    4. Show different keyboards for admin users and not-admin users - DONE
    5. Check pictures amount - DONE
    6. work with local ids when deleting and chosing templates - DONE
    7. Create a spam defend decorator - DONE
    8. register check when entering platform - DONE
    9. fix "unlogged_markup" for chats
    10. telegram api error about runtime fix
    11. fix no @username users

## TODO:
    1. Add inline keyboards - DONE
    2. Add "/view" command to view added templates (show only first 20 symbols of generated template) - DONE
    3. Add player "profile" that will be filled during registration (fractions, crit dmg) - DONE
    4. Add mentioning based on fraction - DONE
    5. Add "description" to template while creating to show it instead of full template - DONE
    6. Add picture handling that is sent with text when creating template or sending message immideatly - DONE
    7. Add group_chat keyboard (consist only fraction and everyone mentions) - DONE
    8. Add pawns mention (banshee, tesla, robot, panda) - DONE
    9. Add ability to edit profile - DONE
    10. Add base commands for Dev-only (reboot, stats, adduser (straight to database))
    11. Add /bug command, that will ease bug-report process
    12. Add strategies for different modifiers
    13. Add some info about items, pawns and etc...
