from database import load_csv


class FakeDatabaseSession:
    def __init__(self):
        self.executed_queries = []
        self.committed = False
        self.rolled_back = False

    def execute(self, query, data=None):
        self.executed_queries.append((query, data))

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


def test_database_import_reads_and_inserts_csv(tmp_path, monkeypatch):
    data_directory = tmp_path / "data"
    data_directory.mkdir()

    csv_file = data_directory / "energydata_complete.csv"

    csv_file.write_text(
        "date,Appliances,lights,T1,RH_1,T2,RH_2,T3,RH_3,"
        "T4,RH_4,T5,RH_5,T6,RH_6,T7,RH_7,T8,RH_8,"
        "T9,RH_9,T_out,Press_mm_hg,RH_out,Windspeed,"
        "Visibility,Tdewpoint,rv1,rv2\n"
        "2016-01-11 17:00:00,60,30,19.89,47.60,19.20,44.79,"
        "19.79,44.73,19.00,45.57,17.17,55.20,7.03,84.26,"
        "17.20,41.63,18.20,48.90,17.03,45.53,6.60,733.50,"
        "92.00,7.00,63.00,5.30,13.27,13.27\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        load_csv,
        "PROJECT_ROOT",
        tmp_path,
    )

    fake_db = FakeDatabaseSession()

    load_csv.load_users_from_csv(fake_db)

    assert fake_db.committed is True
    assert fake_db.rolled_back is False

    assert len(fake_db.executed_queries) == 2

    inserted_data = fake_db.executed_queries[1][1]

    assert len(inserted_data) == 1
    assert inserted_data[0]["Appliances"] == 60
    assert inserted_data[0]["T1"] == 19.89
    assert inserted_data[0]["RH_out"] == 92.0
    assert inserted_data[0]["date"].hour == 17
    assert inserted_data[0]["date"].minute == 0