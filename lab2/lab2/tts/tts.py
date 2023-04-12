#!/usr/bin/python3
# -*- coding: utf-8 -*-

end = None

import pyttsx3 as tts

def main():
  engine = tts.init()
  engine.setProperty('volume',0.7)
  engine.setProperty('rate',190)

  while True:
    tekst = input('>>')
    engine.say(tekst)
    engine.runAndWait()
  end
end

################################################################################

main()

################################################################################
