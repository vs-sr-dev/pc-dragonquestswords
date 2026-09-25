// Dragon Quest Swords — the port's own layer over the wiikit runtime.
//
// Linked into wiiboot by dqs.cmake. What belongs here is what only this
// game needs: its SDK's shapes, and later the sword on the mouse.
#include "rt.h"

namespace {

void install() {
    // the 2007 SDK's KPADStatus is 0x84 bytes (03-executable.md); the game
    // reads 16 of them a frame at 800167E8
    wpad_set_kpad_status_size(0x84);
}

RtGameLayer layer("Dragon Quest Swords", install);

}  // namespace
