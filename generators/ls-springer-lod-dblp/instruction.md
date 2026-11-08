# Instruction: judging the dblp ids of the Springer series

Each line of the evidence is one link: a conference series of the Springer LOD data (2018) and the dblp venue that
Springer gave as its DBLP id. The evidence of the Springer side: the series key (the end of its IRI), its name, and up
to five of its conferences (name, acronym, year, city). Of the dblp side: the venue key, its title, its former titles,
and up to five of its proceedings (year, title), spread over the years.

Judge from this evidence only: do the Springer series and the dblp venue stand for the same series?

- **correct:** the same series. A renamed series is the same series: the former titles of dblp, the titles of its
  proceedings, or the names of the Springer conferences show the rename (e.g. a workshop that became a conference, a
  seminar series that changed its name). Differences in wording, language or abbreviation do not matter. A dblp venue
  whose proceedings are those of the Springer conferences (same name, acronym, years) is the same series even if the
  venue title is worded differently.
- **wrong:**
  - a different series that only shares an acronym or a key (the names and the proceedings point to another topic);
  - a workshop series linked to the venue of its host conference, or a conference linked to the venue of a workshop
    held with it;
  - a series linked to a broader umbrella or catch-all venue (e.g. the publications of an IFIP working group that
    hold several series, a venue that collects several different conference series).
- **undecidable:** the evidence does not tell: the names are too generic or too different to compare and the
  proceedings do not help. Do not guess.

Be strict about the level (workshop vs host conference, one series vs an umbrella), lenient about wording.

Output: one line per link, tab-separated: `i`, `verdict` (correct, wrong or undecidable), `reason` (a few words;
required for wrong and undecidable).
