from pygame import mixer

mixer.init()

move_self = mixer.Sound("rsc/audio/move-self.mp3")
capture = mixer.Sound("rsc/audio/capture.mp3")
dic_sound = {
    1: move_self,
    2: capture
}

def MixerPlay(id):
    mixer.Sound.play(dic_sound[id])