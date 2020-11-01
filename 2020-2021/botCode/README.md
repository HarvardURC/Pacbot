# BotCode

This is the code that runs on the pacbot! There are a few important files on the top level, but most of of the code is sorted into the directories.

#### Specific File Descriptions
- _Master.hpp_: This file contains a static class with a start() method. Once the start() method is called, Master will call an on_init method, and then continously call the on_tick method every tick. All the work that is supposed to happen all the time should be called through this file. Most work that isn't called through this file will be triggerred by server messages.
