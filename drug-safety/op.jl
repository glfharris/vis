using Requests, JSON, DataFrames, Gadfly, Plots

url = "https://openprescribing.net/api/1.0/"

function action(action; query::Dict{String, String}=Dict())
  payload = Dict("format" => "json")
  merge!(payload, query)
  return get(string(url, action), query=payload).data |> String |> JSON.parse
end

function drug(query::String; exact="false", kind="any", select="any")
  res = action("bnf_code", query=Dict("q" => query, "exact" => exact))
  if kind != "any"
    filter!(x -> x["type"] == kind, res)
  end
  if select != "any"
    map!(x -> x[select], res)
  end
  return res
end

function drug(query::Array; exact="false", kind="any", select="any")
  res = []
  for x in query
    append!(res, drug(x, exact=exact, kind=kind, select=select))
  end
  return unique(res)
end

function spending(query::String)
  res = action("spending", query=Dict("code" => query))
  name = replace(drug(query, kind="chemical")[1]["name"], "&", "+") # & causes parsing to go to shit
  df = DataFrame(code=String[], items=Int64[], actual_cost=Float64[], date=Date[], quantity=Int64[], name=String[])
  for x in res
    push!(df, [query x["items"] x["actual_cost"] Date(x["date"], "y-m-d") x["quantity"] name])
  end
  return df
end

function spending(query::Array)
  df = DataFrame(code=String[], items=Int64[], actual_cost=Float64[], date=Date[], quantity=Int64[], name=String[])
  for x in query
    append!(df, spending(x))
  end
  return df
end

df = drug("Aliskiren", kind="chemical", select="id") |> spending
p = Gadfly.plot(df, x=:date, y=:items, color=:name,
    Geom.line,
    Guide.ylabel("Prescriptions per Month"), Guide.xlabel("Date"),
    Coord.cartesian(ymin=0, xmin=minimum(df[:date])))
draw(SVGJS("final/aliskiren.svg", 12inch, 6inch), p)
display(p)
