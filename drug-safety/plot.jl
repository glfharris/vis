using JSON, Requests, Gadfly, Dates

open("alerts.json", "r") do f
    global alerts
    txt = readstring(f)
    alerts = JSON.parse(txt)
    println("Completed Alerts")
end

import Gadfly.optimize_ticks
function TightTicks(data::AbstractArray)
    tmin = minimum(data)
    tmax = maximum(data)
    ticks, trash = Gadfly.optimize_ticks(tmin, tmax)
    ticks = ticks[(ticks.<=tmax)&(ticks.>=tmin)]
end

function plot_drug(drug)
        Gadfly.push_theme(:default)
        name = get_name(drug)
        println("Starting: ", name)
        data = get("https://openprescribing.net/api/1.0/spending", query=Dict("format" => "json", "code" => drug)).data |> String |> JSON.parse
        items = []
        dates = []
        for x in data
            try
                push!(items, x["items"])
                push!(dates, Dates.Date(x["date"], "y-m-d"))
            end
        end
        items::Array{Int64} = map(x -> Int(x), items)
        if length(items) > 0
          if maximum(items) > 200
            try
              start = Dates.Date("2010-01-01", "y-m-d")
              fin = Dates.Date("2016-10-01", "y-m-d")
              intercepts = map(x -> Dates.Date(x, "y-m-d"), alerts[drug])
              p = plot(x=dates, y=items, xintercept=intercepts, Geom.line, Geom.vline(color=colorant"red"), Guide.xlabel("Date"),
              Guide.ylabel("Prescriptions per Month"), Coord.cartesian(xmin=minimum(dates), ymin=0))
              draw(SVG(string("svgs/", name, ".svg"), 12inch, 6inch), p)
              println("Completed: ", name, " At: ", Dates.now())
            end
          else
            println(name, " too small to bother with")
          end
        else
          println(name, " not enough data")
        end
end

function get_name(drug_code)
    res = get("https://openprescribing.net/api/1.0/bnf_code", query=Dict("format" => "json", "q" => drug_code, "exact" => "true")).data |> String |> JSON.parse
    return res[1]["name"]
end

for key in keys(alerts)
    plot_drug(key)
end
