# HOLMES V

HOLMES V is an enhanced version of [HolmesIV](https://github.com/HelloChatterbox/HolmesIV)
  
## Install

The main assumption of HolmesV is that you may want to run only some pieces of the mycroft stack, this means the requirements vary wildly depending on the use case.

eg, if you are making a web chatbot you do not want the audio stack at all

by default HolmesV will only install the bare minimum requirements common to all individual services

```bash
pip install HolmesV==2021.9.8
```

you can perform a full recommended install with
```bash
pip install HolmesV[all]==2021.9.8
```

### Additional requirements

#### Skills

the skills service is the most customizable

msm and padatious needs to be explicitly installed, automatically disabled if unavailable

```bash
pip install HolmesV[skills]==2021.9.8
```

#### Bus

if you want to run the messagebus (instead of connecting to an existing one)
```bash
pip install HolmesV[bus]==2021.9.8
```

#### Enclosure/GUI

if you want to run the enclosure service in order to connect mycroft-gui

```bash
pip install HolmesV[enclosure]==2021.9.8
```

#### STT

if you want to perform speech recognition
```bash
pip install HolmesV[stt]==2021.9.8
```

to install optional STT engines (google cloud)
```bash
pip install HolmesV[stt_engines]==2021.9.8
```

#### TTS
to install optional TTS engines (gTTS)
```bash
pip install HolmesV[tts_engines]==2021.9.8
```

#### Audio Service

if you want to install optional audio backends (vlc + pychromecast)
```bash
pip install HolmesV[audio_engines]==2021.9.8
```


## Compatibility

**you can only install one of HolmesV, HolmesIV or mycroft-core**, they can not run side by side, each of those is an enhanced version of the former

Because Holmes is a drop in replacement that means `import mycroft` would conflict between alternative versions

HolmesV runs skills made for mycroft-core and interfaces with all known mycroft projects, see the [awesome-mycroft-community](https://github.com/ChanceNCounter/awesome-mycroft-community) for a selection of projects that you can integrate with HolmesV
 