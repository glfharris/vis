# MHRA-Updates
Some scripts to visualize responses to MHRA drug safety updates using the Open Prescribin API. Used on www.glfharris.com

#### Usage
It's a mix of Julia and Python because I'm trying to learn Julia some more, and Gadfly is great. Unfortunately webscraping in Julia is a right pain, so I've resorted back to python for some bits.

The key bits are mostly in `op.jl` and plotting a drug is as easy as:

```Julia
df = drug("Aliskiren", kind="chemical", select="id") |> spending
p = Gadfly.plot(df, x=:date, y=:items, color=:name,
    Geom.line,
    Guide.ylabel("Prescriptions per Month"), Guide.xlabel("Date"),
    Coord.cartesian(ymin=0, xmin=minimum(df[:date])))
draw(SVGJS("aliskiren.svg", 12inch, 6inch), p)
```
