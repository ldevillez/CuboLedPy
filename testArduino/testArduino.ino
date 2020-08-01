#include "FastLED.h"
#include "Output.h"
#define NUM_LEDS nbSegment *nbLedSegment
CRGB leds[NUM_LEDS];
void setup()
{
  FastLED.addLeds<NEOPIXEL, 6>(leds, NUM_LEDS);
}

void loop()
{
  for (int stp = 0; stp < nbStep; stp++)
  {
    for (int seg = 0; seg < nbSegment; seg++)
    {
      for (int led = 0; led < nbLedSegment; led++)
      {
        int idx = seg * nbLedSegment + led;
        leds[idx].r = segments[seg][led][stp * 3];
        leds[idx].g = segments[seg][led][stp * 3 + 1];
        leds[idx].b = segments[seg][led][stp * 3 + 2];
      }
    }
  FastLED.show();
  FastLED.delay(delayStep);
  }
}
