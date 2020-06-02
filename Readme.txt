bot name:  	botIntro
username:	bobylev_bot

It is the example of telegram bot.
This bot presents a task list application.

/start
  |
  |
  +-- [new task]
  |      |
  |      +-- add descr --+-- add date --+--[update] --> goto <add descr>
  |                      |              |
  |                      +--[calendar]  +--[save] --+--[home] --> goto </start>
  |                                     |           |
  |                                     +--[cancel] +--[new task] --> goto <new task>
  +-- [my tasks]
          |
          +--[all tasks]
          |
          +--[today tasks]
          |
          +--[tomorrow tasks]
          |
          +--[home]