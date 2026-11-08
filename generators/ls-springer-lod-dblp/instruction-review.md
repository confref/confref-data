# Instruction for the second pass: the links decided differently

The first pass judged every link by `instruction.md`. These links were decided differently: by the first pass and
by the sample judged before, or by judges who applied the rules on umbrella venues and mixed series in different
ways. Judge them again from the evidence of the line only, by `instruction.md` with these added rules, so that the
same rules hold for all links:

1. **Same umbrella on both sides:** if the Springer series is itself a federated or umbrella event (e.g. a congress
   of several conferences) and the dblp venue is the same umbrella, the link is correct.
2. **A dblp venue with a main line:** if the venue's title, former titles and most of its proceedings are one series
   (renames included) and only a few proceedings belong to other, related events (satellite workshops, sister
   conferences), the venue is that series: correct if it is the Springer series. It is an umbrella (wrong) only
   if it has no main line: it collects several different series (the publications of an IFIP working group, a
   series of advanced courses, a collection of workshops).
3. **A Springer series that mixes series:** follow the series name and most of its conferences; one stray
   conference of another series does not change the judgement. If the name and most conferences point to different
   series, the link is undecidable.
4. **A workshop held at a conference** (the Springer series is the workshops of a conference, or a workshop series)
   linked to the conference venue is wrong, also if the workshop name contains the conference acronym.
5. **No name to compare:** if the Springer name says nothing (e.g. only "Conference"), judge by the conferences and
   their acronyms; if they match the dblp proceedings, correct.
6. **A rename** is shown by the evidence (dblp former titles, the proceedings, the names of the Springer
   conferences). Without such evidence, completely different names are undecidable, not correct.
