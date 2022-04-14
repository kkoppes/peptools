def get_all_files(input_folder, a_c_family=["SA", "LR", "DD", "XW", "MT"], hexing=True):
    """
    @param input_folder: folder where all csvs are stored
    @return: dataframe with all concession details
    """
    list_of_files = list_from_folder(input_folder)
    # list_of_files = glob.glob(input_folder + '*.csv')
    # exclude temp files
    # list_of_files = [ x for x in list_of_files if "$" not in x ]

    # Parsing the date column in the dataframe.
    mydateparser = lambda c: pd.to_datetime(c, format="%d.%m.%Y", errors="coerce")
    # date_parser=mydateparser

    dfs = []
    for filename in list_of_files:
        # read in dataframe
        if os.stat(filename).st_size > 100:
            logging.info(filename)
            df = pd.read_csv(
                filename,
                delimiter=";",
                decimal=",",
                thousands=".",
                parse_dates=["Creation Date", "Quality Date", "Non Acceptation Date"],
                date_parser=mydateparser,
            )
            dfs.append(df)

    df_data = pd.concat(dfs, axis=0, ignore_index=True)

    # clean columns
    df_data = clean_col_nms(df_data)
    if hexing == True:
        # hash encode names
        df_data.task_resp__name = df_data.task_resp__name.apply(lambda x: do_hash(x))
        # hash encode users
        df_data.task_resp_user = df_data.task_resp__name.apply(lambda x: do_hash(x))

    # fix numeric columns
    df_data[["sum_ttc_cal__days", "sum_tta_cal__days", "quality_duration"]] = df_data[
        ["sum_ttc_cal__days", "sum_tta_cal__days", "quality_duration"]
    ].fillna(0)

    ## copy quality acc date to seperate column
    df_data["quality_date_acc"] = df_data["quality_date"]
    # make date format
    df_data["quality_date_perf"] = pd.to_datetime(
        df_data["quality_date_acc"], format="%d%m%Y", errors="coerce"
    )
    df_data["non_acceptation_date"] = pd.to_datetime(
        df_data["non_acceptation_date"], format="%d%m%Y", errors="coerce"
    )

    df_data["quality_date_perf"] = df_data[
        "quality_date_acc"
    ]  # .combine_first(df_data['non_acceptation_date'])

    # combine columns (fill non-acc date in acc date column to get combined results)
    df_data["quality_date_pq"] = df_data["creation_date"]
    # add year, month week column
    df_data["quality_date_year"] = df_data[
        "quality_date"
    ].dt.year  # create seperate column for year
    df_data["quality_date_month"] = df_data["quality_date"].dt.strftime(
        ("%m %b")
    )  # create seperate column for month
    df_data["quality_date_week"] = df_data[
        "quality_date"
    ].dt.week  # create seperate column for week
    #
    df_data["creation_date_year"] = df_data[
        "creation_date"
    ].dt.year  # create seperate column for year
    df_data["creation_date_month"] = df_data["creation_date"].dt.strftime(
        ("%m %b")
    )  # create seperate column for month
    df_data["creation_date_week"] = df_data[
        "creation_date"
    ].dt.week  # create seperate column for week

    df_data["quality_date_perf_year"] = df_data[
        "quality_date_perf"
    ].dt.year  # create seperate column for year
    df_data["quality_date_perf_month"] = df_data["quality_date_perf"].dt.strftime(
        ("%m %b")
    )  # create seperate column for month
    df_data["quality_date_perf_week"] = df_data[
        "quality_date_perf"
    ].dt.week  # create seperate column for week

    # deal with year overlapping weeks based on isocalender
    for datestr in ["quality_date", "creation_date", "quality_date_perf"]:
        # if last week laps over in jan
        df_data.loc[
            (df_data[f"{datestr}_month"] == "01 Jan")
            & (df_data[f"{datestr}_week"].isin([52, 53])),
            f"{datestr}_year",
        ] -= 1
        # if first week laps over in dec
        df_data.loc[
            (df_data[f"{datestr}_month"] == "12 Dec")
            & (df_data[f"{datestr}_week"] == 1),
            f"{datestr}_year",
        ] += 1

    df_data["post_box"] = df_data.task_resp__team.str.strip().str[-8:]

    df_data["fact_code"] = df_data["concession_number"].str.extract(
        "([a-zA-Z]{2,3})", expand=True
    )
    # entries without concessions (deleted)
    df_data = df_data[~df_data.fact_code.isna() == True]
    # filter out removed data #
    df_data = df_data[~(df_data["quality_date_year"] == "NaT")]
    df_data = df_data[~(df_data["creation_date_year"] == "NaT")]

    # todo: clarify WB (A300 - 310) concessions? up to then not taken into account
    df_data = df_data.loc[df_data["a_c_family"].isin(a_c_family)]

    # remove duplicated entries
    df_data = df_data.drop_duplicates()

    logging.info(f"there are {len(df_data)} records")
    return df_data
