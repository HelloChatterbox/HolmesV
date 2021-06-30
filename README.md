# HOLMES IV

HOLMES IV (formerly [mycroft-lib](https://mycroft.ai/trademark/)) is a repackaged version of [mycroft-core](https://github.com/MycroftAI/mycroft-core/)

`Mike, alias Adam Selene, alias Simon Jester, alias Mycroft Holmes, officially an augmented HOLMES IV system, is a supercomputer empowered to take control of Lunar society, which achieved self-awareness`

`HOLMES IV` is named after the `HOLMES IV` system from the novel `The Moon is a Harsh Mistress` by `Robert Heinlein`, It is the system the next generation of voice assistants will be built on top of

It is aimed at developers and makers interested in building on top of the mycroft stack, if you are a end-user that just wants to install mycroft please see the [official repository](https://github.com/MycroftAI/mycroft-core/)

For an enhanced version checkout the successor project [HolmesV](https://github.com/HelloChatterbox/HolmesV)

- [HOLMES IV](#holmes-iv)
  * [Features](#features)
  * [Objectives](#objectives)
  * [Install](#install)
  * [Compatibility](#compatibility)
  
## Features

HolmesIV tries to be a drop-in replacement for mycroft-core, most changes are just cleanup and moving imports around, however there are some notable new configuration options:

| Feature                               | Mycroft                              | HolmesIV                               |
|---------------------------------------|--------------------------------------|----------------------------------------|
| backend                               | required                             | optional                               |
| internet connection                   | required                             | optional                               |
| msm                                   | required                             | optional                               |
| padatious                             | required                             | optional                               |
| ntp sync                              | hardcoded list of platforms (forced) | optional                               |


## Objectives

- facilitate the development of projects on top of the mycroft-core
- repackage mycroft-core as a library that can be easily distributed
- modularize mycroft-core into small reusable components
- minimize the amount of dependencies required for a given setup
- maximize the amount of platforms HolmesIV can be used on
- do not break the established mycroft-core API other projects rely on
- transparently load skills developed for mycroft-core
- transparently integrate with any project developed to interface with mycroft-core
- it should always be possible to run HolmesIV with the same exact configuration as mycroft-core, given that all system requirements are met
- versioning should indicate the state of HolmesIV synchronization with mycroft-core
   - main version number is the date of last sync with dev branch on mycroft-core
  

## Install

The main assumption of HolmesIV is that you may want to run only some pieces of the mycroft stack, this means the requirements vary wildly depending on the use case.

eg, if you are making a web chatbot you do not want the audio stack at all

by default HolmesIV will only install the bare minimum requirements common to all individual mycroft services

```bash
pip install HolmesIV==2021.9.8a1
```

you can perform a full recommended install with
```bash
pip install HolmesIV[all]==2021.9.8a1
```

### Additional requirements

#### Skills

the skills service is the most customizable

msm and padatious needs to be explicitly installed, automatically disabled if unavailable

```bash
pip install HolmesIV[skills]==2021.9.8a1
```

#### Bus

if you want to run the messagebus (instead of connecting to an existing one)
```bash
pip install HolmesIV[bus]==2021.9.8a1
```

#### Enclosure/GUI

if you want to run the enclosure service in order to connect mycroft-gui

```bash
pip install HolmesIV[enclosure]==2021.9.8a1
```

#### STT

if you want to perform speech recognition
```bash
pip install HolmesIV[stt]==2021.9.8a1
```

to install optional STT engines (google cloud)
```bash
pip install HolmesIV[stt_engines]==2021.9.8a1
```

#### TTS
to install optional TTS engines (gTTS)
```bash
pip install HolmesIV[tts_engines]==2021.9.8a1
```

#### Audio Service

if you want to install optional audio backends (vlc + pychromecast)
```bash
pip install HolmesIV[audio_engines]==2021.9.8a1
```

  
## Compatibility

**you can only install one of HolmesV, HolmesIV or mycroft-core**, they can not run side by side, each of those is an enhanced version of the former

Because Holmes is a drop in replacement that means `import mycroft` would conflict between alternative versions

HolmesIV runs skills made for mycroft-core and interfaces with all known mycroft projects, see the [awesome-mycroft-community](https://github.com/ChanceNCounter/awesome-mycroft-community) for a selection of projects that you can integrate with HolmesIV
 