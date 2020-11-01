# BotCode

This is the code that runs on the pacbot! There are a few important files on the top level, but most of of the code is sorted into the directories.

#### Specific File Descriptions
- _Master.hpp_: This file contains a static class with a start() method. Once the start() method is called, Master will call an on_init method, and then continously call the on_tick method every tick. The tick length can be found in Master.cpp
