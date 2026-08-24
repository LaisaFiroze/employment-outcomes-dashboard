// Power Query (M) - cleans and reshapes the raw case management export
// before it hits the data model.

let
    Source = Csv.Document(File.Contents("sample_client_events.csv"), [Delimiter=",", Columns=8, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // fix data types coming in from the raw export
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"client_id", type text},
        {"engagement_date", type date},
        {"sector", type text},
        {"referral_source", type text},
        {"adviser", type text},
        {"current_stage", type text},
        {"placed_date", type date},
        {"days_on_programme", Int64.Type}
    }),

    // drop exact duplicate rows - re-referrals sometimes create these
    RemovedDuplicates = Table.Distinct(ChangedTypes),

    // add a flag for whether the client has reached placement, used
    // downstream for the placement rate KPI
    AddedPlacedFlag = Table.AddColumn(RemovedDuplicates, "is_placed", each
        if [placed_date] <> null then 1 else 0, Int64.Type),

    // add a sustainment flag for the 26-week KPI card
    AddedSustainedFlag = Table.AddColumn(AddedPlacedFlag, "is_sustained_26wk", each
        if [current_stage] = "Sustained (26 weeks)" then 1 else 0, Int64.Type),

    // trim whitespace introduced by manual data entry in the source system
    TrimmedText = Table.TransformColumns(AddedSustainedFlag, {
        {"sector", Text.Trim, type text},
        {"adviser", Text.Trim, type text}
    })

in
    TrimmedText
