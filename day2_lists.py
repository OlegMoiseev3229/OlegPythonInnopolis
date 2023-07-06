import re
import time

import matplotlib.pyplot as plt
from func_stuf import cache


def keep_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        return result, t2 - t1
    return wrapper


def create_the_matrix(n):
    matrix = [[0]*5 for _ in range(n)]
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if x == y:
                matrix[y][x] = 1
            else:
                matrix[y][x] = x + y
    return matrix


def read_to_dict(the_dict: dict, text: str):
    words_list = split_str(text)
    for word in words_list:
        word = word.lower()
        the_dict[word] = the_dict.get(word, 0) + 1
    return the_dict


def get_text():
    text = input("Your text >>>")
    if text == "":
        text = """Jan pi sona ala, [04.07.2023 9:50]
My name is Fritz Zwicky,
I can be kind of prickly.
This song had better start by giving me priority.
Whatever anybody says,
I said in 1933.
Observe the Coma cluster,
the redshifts of the galaxies imply some big velocities.
They’re moving so fast, there must be missing mass!
Dark matter.
Dark matter: Do we need it? What is it? Where is it? How much?
Do we need it? Do we need it? Do we need it? Do we need it?
For nearly forty years,
the dark matter problem sits,
And nobody gets worried ’cause “It’s only crazy Fritz.” The next step’s not ’til the early 1970s,
Ostriker and Peebles,
dynamics of the galaxies,
cold disk instabilities.
They say: “If the mass, were sitting in the stars,
all those pretty spirals, ought to be bars!
Self-gravitating disks? Uh-uh, oh no.
What those spirals need is a massive halo.” “And hey, look over here, check out these observations,
Vera Rubin’s optical curves of rotation,
they can provide our needed confirmation:
Those curves aren’t falling, they’re FLAT!
Dark matter’s where it’s AT!
Dark matter: Do we need it? What is it? Where is it? How much?
What is it? What is it? What is it? What is it?
And so the call goes out for the dark matter candidates:
black holes, snowballs, gas clouds, low mass stars, or planets
But we quickly hit a snag because galaxy formation requires too much structure in the background radiation if there’s only baryons and adiabatic fluctuations.
The Russians have an answer: “We can solve the impasse.
Lyubimov has shown that the neutrino has mass.” Zeldovich cries, “Pancakes! The dark matter’s HOT.” Carlos Frenk, Simon White, Marc Davis say, “‘NOT!
Quasars are old, and the pancakes must be young.
Forming from the top down it can’t be done.” So neutrinos hit the skids, and the picture’s looking black.
But California laid-back, Blumenthal & Primack say, “Don’t have a heart attack.
There’s lots of other particles.
Just read the physics articles.” “Take this pretty theory that’s called supersymmetry.
What better for dark matter than the L-S-P?
The mass comes in at a ∼ keV,
and that’s not hot, that’s warm.” Jim Peebles says, “Warm? Don’t be half-hearted.
Let’s continue the trend that we have started.
I’ll stake out a position that’s bold:
dark matter’s not hot, not warm, but COLD.” Well cold dark matter causes overnight sensations:
hand-waving calculations,
computer simulations,
detailed computations of the background fluctuations.
Results are good, and the prospects look bright.
Here’s a theory that works!
Well, maybe not quite.
Dark matter: Do we need it? What is it? Where is it? How much?
Where is it? How much? Where is it? How much?
We have another puzzle that goes back to Robert Dicke.
Finding a solution has proven kind of tricky.
The CMB’s so smooth, it’s as if there’d been a compact between parts of the universe that aren’t in causal contact.
Alan Guth says, “Inflation,
will be our salvation,
give smoothness of the universe a causal explanation,
and even make the galaxies from quantum fluctuations!” “There is one prediction, from which it’s hard to run.
If inflation is correct, then Omega should be one.”
Observers say, “Stop, no, sorry, won’t do.
Check out these clusters, Omega’s point 2.” The theorists respond, “We have an explanation.
The secret lies in biased galaxy formation.
We’re not short of critical mass density.
Just some regions, are missing luminosity.” Observers roll their eyes, and they start to get annoyed,
But the theorists reply, “There’s dark matter in the voids.” Dark matter: Do we need it? What is it? Where is it? How much?
Do we need it? Do we need it? Do we need it? Do we need it?
Along comes Moti Milgrom, who’s here to tell us all:
“This dark matter claptrap has got you on the wrong track.” “You’re all too mired in conventionality,
wedded to your standard theory of gravity,

Jan pi sona ala, [04.07.2023 9:50]
seduced by the elegance of General Relativity.
Just change your force law, that’s the key.” “Give me one free parameter, and I’ll explain it all.” “Not so,” claim Lake, and Spergel, et al.,
“On dwarfs, and lensing, your theory’s gonna fall.” The argument degenerates; it’s soon a barroom brawl.
Dark matter: Do we need it? What is it? Where is it? How much?
What is it? What is it? What is it? What is it?
New observations hit the theory like an ice cold shower.
They show that cold dark matter has too little large scale power.
Says Peebles: “Cold dark matter? My feeblest innovation.
An overly aesthetic, theoretical aberration.
Our theories must have firmer empirical foundation.
Shed all this extra baggage, including the carry-ons.
Use particles we know, i.e., the baryons.” Others aren’t convinced, and a few propose a mixture of matter hot and cold, perhaps with strings or texture.
But nowadays most physicists are captured by the synergy of inflation, cold dark matter, and repulsive dark energy.
Lambda or quintessence makes the whole picture integrate by causing the expansion of the cosmos to accelerate.
New physics is exciting, and it gives us more to do.
Before we had one mystery, and now we have two.
But still we have to search for those darn elusive particles,
subject every year of a thousand theory articles
WIMPy, fuzzy, warm, dark atomic, superlight,
so hard to find it feels like they are hiding out of spite.
So we huddle deep in mines with the world’s supply of xenon seeking scintillating flashes of the insight we are keen on.
Mic silicon-germanium to listen in for phonons.
Build hyper-volume radios, tuning in for axions.
We search the skies for gamma-rays from WIMP annihilation,
those tiny sparks that light the dark in EM radiation.
We smash together protons, search for tracks in the debris,
to prove we made our own DM within the LHC.
The search is ever-popular, as many realize that the detector of dark matter may well win the Nobel Prize.
So now you’ve heard my lecture, and it’s time to end this session with the standard closing line: Thank you, any question"""
    elif text == "import this":
        text = """The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""
    elif text == "BB":
        text_list = []
        with open("1984 pdf_djvu.txt", "r", encoding="UTF-8") as f:
            i = 0
            while True:
                if i >= 30000:
                    break
                i += 1
                try:
                    text_list.append(f.readline())
                except UnicodeDecodeError:
                    continue
        text = "\n".join(text_list)

    return text


def split_str(string, sep="\s+"):
    if sep == '':
        return (c for c in string)
    else:
        return (_.group(1) for _ in re.finditer(f'(?:^|{sep})((?:(?!{sep}).)*)', string))


@keep_time
@cache
def fib(n):
    """Returns the n-th fibonacci number
    fibonacci(0) = 0
    fibonacci(1) = 1
    fibonacci(n) = fibonacci(n - 2) + fibonacci(n - 1)"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    result = fib(n - 2)[0] + fib(n - 1)[0]
    return result


def plot_counts():
    count_dict = read_to_dict(dict(), get_text())
    count_list = [[], [], []]
    i = 0
    for k, v in sorted(count_dict.items(), key=lambda x: x[1], reverse=True):
        print(f"{k}: {v}")
        count_list[0].append(i)
        count_list[1].append(v)
        count_list[2].append(k)
        i += 1
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(count_list[0][:200], count_list[1][:200])  # Plot some data on the axes.
    plt.show()


if __name__ == '__main__':
    times = []
    for i in range(35):
        n, t = fib(i)
        print(i, n)
        times.append(t)
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot([i for i in range(35)], times)  # Plot some data on the axes.
    plt.show()
