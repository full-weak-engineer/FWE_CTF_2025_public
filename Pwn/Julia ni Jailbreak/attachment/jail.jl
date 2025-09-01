function parse(s::String)
    if any(c -> occursin(c, s), ['@', '`'])
        throw(Exception("Forbidden character detected"))
    end
    return Meta.parse(s)
end

function detect_forbidden(expr::Any)
    found = Set{Symbol}()
    function traverse(x)
        if x isa Expr
            traverse(x.head)
            for arg in x.args
                traverse(arg)
            end
        elseif x isa Symbol
            if x in Set(append!(names(Base, all=true), names(Core, all=true), [:import])) && !(x in [:!, :!=, :!==, :%, :&, Symbol("'"), :*, :+, :-, :/, ://, :(:), :<, :<:, :<<, :<=, :(==), :(=>), :>, :>:, :>=, :>>, :>>>,:|, :|>, :~, :÷, :π, :ℯ, :∈, :∉, :∋, :∌, :∘, :√, :∛, :∜, :∩, :∪, :≈, :≉, :≠, :≡, :≢, :≤, :≥, :⊆, :⊇, :⊈, :⊉, :⊊, :⊋, :⊻, :⊼, :⊽, :\, :^, :Array, :Float16, :Float32, :Float64, :UInt, :UInt128, :UInt16, :UInt32, :UInt64, :UInt8,:Int, :Int128, :Int16, :Int32, :Int64, :Int8, :pointer_from_objref, :undef, :println, :parse, :chop, :repr, :pointer, :head, :tail, :Base])
                print(x)
                push!(found, x)
            end
        elseif x isa QuoteNode
            traverse(x.value)
        end
    end
    traverse(expr)
    return !isempty(found)
end

println("Enter julia code> ")
expr = parse(readline())
if detect_forbidden(expr)
    println("Forbidden symbol found")
else
    Core.eval(Main, expr)
end