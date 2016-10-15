Date: 01-01-2000
Title: SolarEnergy
Type: wiki



<span style="color: red;">Beware back of the envelope calculations &
random Frosty musings.</span>





### Current Situation \[Sept 2008\]

Club currently owns a 13W amorphous silicon briefcase type panel
(sunshine solar), a semi-working old 20W BPSolar (or similar) semi-flex
panel \[left in Bivi, producing \~6-10W 2008\]. Also have two broken
semi-flex 20W panels. The individual cells are almost certainly good -
died due to corrosion.

Small (12Ahr) lead acid club battery is believed dead due to
sulpification (sic).





### Lead Acid

Lead acid car battery has energy density of: 25 Wh/kg

<http://wiki.xtronics.com/index.php/Energy_density>





### Drill Packs

Typical power content seems to be \~30Whr

Ref: Relatively modern ryobi one+ system consists of 18V 1.7Ah
batteries.





### Solar Flux on Mig?

Well from Lat & Long, one expects \~1100 Kwh in a year per Kw peak
production panels (0.7 efficiency of system, ideal fixed orientation
blah blah). Ref:
<http://newenergynews.blogspot.com/2007/05/mediterranean-sun.html>

Of course, we're there in the summer. But we're also under a personal
cloud most of the time, so this figure is probably roughly correct for
the expo power average.

This gives us a ballpark DAILY figure of 3Whr / 1W peak panels. \~1/4Ahr
@12V for 1W peak





### Ideal Location / Alignment

Putting the panel outside a tent to run as 'charging station' seemed to
make a lot of sense, rather than relying on people fetching the battery
+ panel from the bivi every morning.

We are there just after high summer, so what would be the ideal angle to
orientate the panel at? And given the weird weather on mig (crystal
clear dawns, clouding over 11am or sometimes starting klag, burning off
midday etc.), is there a more optimal (non south-facing) direction for
our panels?

And is there a better tracker we could build than freshers?





### Source of new panels

So we have those two dead panels. So why not peel them open and build
our own ghetto modules? Building ref / howto:
<http://www.instructables.com/id/Make-a-high-powered-solar-panel-from-broken-solar-/>

We should probably at least try this before blowing any more money.

<http://www.sunshinesolar.co.uk/> are where we bought the briefcase; 40W
amorphous (12kg!) modules for Ł150 (special deal, Sept 08)





### Alternative Power Sources

Petrol generators = heavy, smelly, dirty, fail often, expensive.

But surely there must be some kind of way we can build a beautifully
elegant dwarf-pine fuelled Stirling engine battery charger?





### Direct Charging from Solar

Nice 0.5V (low drop) --&gt; fixed to 12V regulator chip from National
Semiconductors (LM2940). Also available to 5V (i.e. to power USB socket
for various gizmos, Nokia etc.). Difficult to source the chips, the REUK
website has lower costs than Farnell from USA!

Circuit below seems to have a seriously under-rated capacitor (100uF).

Ref: <http://www.reuk.co.uk/LM2940-12V-1A-Low-Dropout-Regulator.htm>
