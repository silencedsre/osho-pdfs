import time
import base64
import requests
import streamlit as st
from pathlib import Path


def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


pdf_list = [
    ("179_Zen_The_Special_Transmission.pdf", "1UCuMRJB_BAwng8CzxNMCA_8oQSJv5hrm"),
    ("180_Zen_Zest_Zip.pdf", "1T3nH-A4-pcXx0k-l3TRfOc0V5OrNd0eG"),
    ("178_Zen_The_Solitary_Bird.pdf", "1HStQxf7JoGxcBlE1lcy3NbIdzMKnv970"),
    ("177_Zen_The_Quantum_Leap.pdf", "1iYBwyMPXxP_OfHXh1ay5T4MscHvtZ5xy"),
    ("174_Zen_The_Path_of_Paradox_Vol_1.pdf", "1N61N6-xjUxJGI9_jPlxb4nTXg3x7lSXE"),
    ("176_Zen_The_Path_of_Paradox_Vol3.pdf", "1Ks-c3syhgl-eie70HxlPrMYDqSw_AkHA"),
    ("175_Zen_The_Path_of_Paradox_Vol2.pdf", "19bw0AByA9s58Eu2NmeAPWY8fx8Pal-he"),
    ("173_Zen_The_Mystery_and_The_Poetry.pdf", "1fthrt1HW_-bIoy2TqpODhOIaufWRuDSr"),
    ("172_Zen_The_Diamond_Thunderbolt.pdf", "1e4TXgMAiTFFqClj6Vzgc9jLF6W2E71cq"),
    ("170_Zarathustra_The_Laughing_Prophet.pdf", "1iosJZNoOs0I3BOHI50h_dek_-lI7A7XD",),
    ("171_The_Zen_Manifesto.pdf", "1huj9kFxaGp3tYwFypQhgrJbtlOxzQb6w"),
    ("169_Zarathustra_A_God_That_Can_Dance.pdf", "17jJwJDNTA4x1prEYylAM7RlZbtEHqmAs",),
    ("157_YAA_HOO_The_Mystic_Rose.pdf", "1YNS3j7h_sanWwAtEV-kJ0p5KMENTI2LO"),
    ("156_The_Wisdom_of_the_Sands_Vol2.pdf", "1jFOQSGsY57RT2Wx4VDCemvDbmUqHH5UH"),
    ("148_Vigyan_Bhairav_Tantra_Vol1.pdf", "1nQP3rBbuYjgm-rXhqiCHJMNdIv3NluFd"),
    ("154_The_Wild_Geese_and_the_Water.pdf", "1c_aGqBOjEapXm2X1MjCD6D7cmSl5m11V"),
    ("155_The_Wisdom_of_the_Sands_Vol1.pdf", "101TSgtkaHZ4eGU0zg3t00KzreQNRy2fp"),
    ("153_The_White_Lotus.pdf", "11I9O0xMHahazG_J3sTtGAYjpA3BE4oKe"),
    ("151_Walking_in_Zen_Sitting_in_Zen.pdf", "1a0vcJPAos0RwjAYd9gmkCbOhxHrE5JwN"),
    ("152_When_the_Shoe_Fits.pdf", "1fuO69gvxWFPOqWDOqK51PrhRSVo1QxpD"),
    ("149_Vigyan_Bhairav_Tantra_Vol 2.pdf", "1YkJSjnElXdD2l-s8oqgfduzy5HWYt5Oj"),
    ("150_Walk_Without_Feet.pdf", "1fKwGpchqTAllPEX0NGRsWSTzL8JeREWK"),
    ("147_Vedanta_Seven_Steps_to_Samadhi.pdf", "1JRhT9Q6oQK4AiDIP4liEIv-03CpcZX_w"),
    ("145_Unio_Mystica_Vol2.pdf", "1E9aP2BX-OAmKEC-eoS2ye3tb4baOurJl"),
    ("146_Until_You_Die.pdf", "1SZOIOK9hYWYdXYKC_NUBzRVKc1vIwyX_"),
    ("143_The_Ultimate_Alchemy_Vol2.pdf", "17jgqrZ38VxR1TIZk13NSl08A_K8BcDrb"),
    ("144_Unio_Mystica_Vol1.pdf", "1QOREtbL0yQia6fXhINQwgriaJ5hJcp18"),
    ("142_The_Ultimate_Alchemy_Vol1.pdf", "1qtoz635qQddaWj9G_M21WZpVbZdijnwn"),
    ("141_Turning_In.pdf", "1jEbhe404JInla4z0j0Bf4ZXHBhM0SONh"),
    ("139_The_Transmission_of_the_Lamp.pdf", "1jXsRvZ9cyle94YkPyuos7lEgmWpVR9gc"),
    ("140_The_True_Sage.pdf", "16fTbEJ1XvXwNhMjtZDO6SlviTAYqEiYR"),
    ("138_This_This_A_Thousand_Times.pdf", "1M64DuVWpndn2IUxH9W0Hkw8PtZk364mB"),
    ("136_Theologia_Mystica.pdf", "1hzxKp53Er87bYbs5brTVypctKJJxqVWV"),
    ("137_This_Very_Body_the_Buddha.pdf", "1NCcIXBqzs92BKgxTQ5NF8C2b4QXuce1v"),
    ("135_That_Art_Thou.pdf", "1RMzH5meNcCfIG6iXIIrjspjjKinyLEB8"),
    ("134_Tao_The_Three_Treasures_Vol4.pdf", "1KhJhXCO-BrtddKV7-MdVyyIiwXjXIUuc"),
    ("133_Tao_The_Three_Treasures_Vol3.pdf", "1hJRL7ZlxgRlRr9a9SfgfNkBz4RTU769T"),
    ("132_Tao_The_Three_Treasures_Vol2.pdf", "1e6MdNsuQawhJvO8hisplhTUo673H8rrF"),
    ("131_Tao_The_Three_Treasures_Vol1.pdf", "1chwbWRhR7WIt-qZlbBKYwXXDqoRFiHBF"),
    ("130_Tao_The_Pathless_Path_Vol2.pdf", "19KG_vCxQg1EajqrW59A9C8W3eEqVuJOC"),
    ("127_Tao_The_Golden_Gate_Vol1.pdf", "1Pl637feONeJqkCHiul9k7fe88vMVv7z7"),
    ("129_Tao_The_Pathless_Path_Vol1.pdf", "1X4hkKmUm-SsH4KOD9sPVAtTi1ReEozXA"),
    ("128_Tao_The_Golden_Gate_Vol2.pdf", "1bib6QOywcUr3NptQbRc9Wh52W2hhFW6I"),
    ("126_Tantra_The_Supreme_Understanding.pdf", "1y_ubxUf1bQLCOygvNLJjlI0BGXj-ncq6",),
    ("125_The_Tantra_Vision_Vol2.pdf", "1Y1h5gf4SaxEooV_V1AxrNcd4yEAZQ3Do"),
    ("124_The_Tantra_Vision_Vol1.pdf", "1Wo9TbxYpwlfXgmCBmuMYeCpLyaVXDKHP"),
    ("123_Take_It_Easy_Vol2.pdf", "1UzRDw-Y5iOYJM7BnEqqZs59sKNteQ0T3"),
    ("122_Take_It_Easy_Vol1.pdf", "18lAa3sxSsSDimdFIrvAF2LMW5OA8nRPc"),
    ("116_Socrates_Poisoned_Again.pdf", "1qicgPrl5yGB0r0EtiNZZP8LjMwbikLDM"),
    ("121_The_Sword_and_the_Lotus.pdf", "1NBkChgtRvkOMMIqGj2P0jbVh8g9X3wjq"),
    ("120_The_Supreme_Doctrine.pdf", "1UmFXmjyxCszP3Dir-_tMPtlOjClcQbED"),
    ("117_Sufis_The_People_of_the_Path_Vol1.pdf", "1IByid5RemLOctBGjrmv0Zq8Ov-k0_Ttl",),
    ("118_Sufis_The_People_of_the_Path_Vol2.pdf", "1sSx-n-mLyC1LH_nR0R8x7Utc5qrVvRFa",),
    ("115_Sermons_in_Stones.pdf", "12BD0PexmQIrYcZWvGJcgmUr6cp83Zhot"),
    ("119_The_Sun_Rises_in_the_Evening.pdf", "1BeMJnxeRjU5XklbsemUV_InC2CkWoG_U"),
    ("112_The_Secret.pdf", "1OgGMc_8u31CHTL9VR24vOVyUmwJNKPRM"),
    ("114_The_Secret_of_Secrets_Vol2.pdf", "1vHWCnvW5xrWWAyTLSlqyr-SQSOICKI-Z"),
    ("113_The_Secret_of_Secrets_Vol1.pdf", "1HTAQIsFsjXkZff92LV-hCVqy0mpnf4pn"),
    ("110_Satyam_Shivam_Sundram.pdf", "1lcXkLHAZo3uigv6LgRimLNSSK9l8X0aL"),
    ("111_The_Search.pdf", "1p5yK4Xm_WBcfdSQLCtxhAGq79h8wVmKO"),
    ("109_Sat_Chit_Anand.pdf", "1IIS-ZH6iD9YP0-Qe2lhyQamHGgaWKiGw"),
    ("108_Rinzai_Master_of_the_Irrational.pdf", "1D_A8F7Y9pBTQQlScger4Yw95sUNdejsl",),
    ("107_The_Revolution.pdf", "1iqihA6JH2ljF95j-7-wzPpXzbJQPhk-i"),
    ("106_Returning_to_the_Source.pdf", "1umxn-USrPKVXQwm7Amtg7NnINQkQ-6e1"),
    ("105_The_Rebellious_Spirit.pdf", "1o4MvlkBC_CNyUkEpZ7X05vreV4ShJmtS"),
    ("104_The_Rebel.pdf", "1YShMcIMcN1weO453xCFvXhA_gN_C1rm3"),
    ("103_The_Razors_Edge.pdf", "1kGCz4VMxa5WdVYgKlrE7jnPGe6V3Flcx"),
    ("102_The_Psychology_of_the_Esoteric.pdf", "1xnBxi5Ql1YEFmzpzfaB_6GtSpP7gnQOU"),
    ("100_Philosophia_Ultima.pdf", "1oTMx_ZtCR8Gk4aTFnCB_WR9Vf2a7CZgX"),
    ("099_Philosophia_Perennis_Vol_2.pdf", "1FRXt11BVd4gETBmDI2pYX8UMZsOYh-9L"),
    ("101_Press_Conferences.pdf", "1bQ6_c2wb0ugK4OPEQr43S7hJfGl5sJE1"),
    ("095_The_Path_of_the_Mystic.pdf", "1ELwkxMIASmd17wKciBd1TW3sMbsjGmqS"),
    ("096_The_Perfect_Master_Vol1.pdf", "1WI19IDUG4rVPnedq-GiXvL7TCQJUlSAH"),
    ("098_Philosophia_Perennis_Vol_1.pdf", "1G7GaBdcNDGTwznscjoPzfKsEbF4LCul7"),
    ("097_The_Perfect_Master_Vol2.pdf", "13cV5yxp9Tbo68RAwNUHcmOSHlWVFkVg2"),
    ("093_The_Osho_Upanishad.pdf", "1nWfU_fMZ_U-Zbr_MDL-bL4FG6mCKXh2_"),
    ("094_The_Path_of_Love.pdf", "1cse6r5GIMrt1Mdl1VIr0KLeLmj6Aso49"),
    ("092_The_Original_Man.pdf", "1Cp03sezn_OxYjqaEc85vYnvDGpID6nSP"),
    (
        "091_One_Seed_Makes_the_Whole_Earth_Green.pdf",
        "1eCDWxcaFU_Vvm4LGtf4A-3upuLUAqHiq",
    ),
    ("090_Om_Shantih_Shantih_Shantih.pdf", "1IQyYvEsbHxi6hH_pswhpCckgdjMJchHG"),
    ("089_Om_Mani_Padme_Hum.pdf", "1yjghYzSIrz3HgL8Jsb6eHfyjdLuONeu2"),
    ("086_Nirvana_The_Last_Nightmare.pdf", "1aOYcc__0hJh7qBXaTAPvujwjMY6yPjlg"),
    ("087_No_Mind.pdf", "1zirXDmu0KynG7zgzHyt46_ytZxXUinh0"),
    ("085_The_New_Dawn.pdf", "1zG6fUBcY6Rc5SLoy12mZMlEukQfhEYv1"),
    ("084_The_New_Alchemy.pdf", "1HFvY3ADwSaZcBgd_oRzabgcCfGWdmyX2"),
    ("083_Nansen_The_Point_of_Departure.pdf", "1-aIPb68GZYrdsj4pYDE3lLIlu0sdQBHt"),
    (
        "082_My_Way_The_Way_of_the_White_Clouds.pdf",
        "1GXY750biwz94XeMTwVrkCVFnoVVOz20L",
    ),
    ("081_The_Mustard_Seed.pdf", "1_KE8KZL7nEZCUHonBDP4J_g55ctWxcbI"),
    ("079_The_Messiah_Vol2.pdf", "1fk0tB1N2WLyrzIuJLmbrH9DIzxEzFGM8"),
    ("080_The_Miracle.pdf", "1twGgu9CZIDBkLM-tOCMNObEC7sUZ-o2z"),
    ("078_The_Messiah_Vol1.pdf", "1h-UAXGRp6sWRnwGSDRdqWxC2AXB_4rfb"),
    ("077_Ma_Tzu_The_Empty_Mirror.pdf", "1vg86OfFaMFfzSz_DUrQ_bJ6Uc7Sm3lqo"),
    ("075_Light_on_the_Path.pdf", "1Owh3sg8JYNuYmF4JUw98g9sWUtEVTiNW"),
    ("076_Live_Zen.pdf", "1r5VhuNuyKo_ZLsSVAOi7D-7Z03oGtLAp"),
    ("068_The_Language_of_Existence.pdf", "1cSkmkG9gPzgxYghTdQQbmaWrqwNrhrki"),
    ("062_The_Invitation.pdf", "1_-dKeiUuNY8MFicMdqJByYybCtpxuqOO"),
    ("067_Kyozan_A_True_Man_of_Zen.pdf", "15ctorQ0k-ozYj15PabRItZyovRoql8Kw"),
    ("066_Just_Like_That.pdf", "1hmVg2NXOCG5dEh4H23jvazRsqR2EB0lT"),
    ("065_Joshu_The_Lions_Roar.pdf", "1x9nt_fCbY9twz-K86Q87QzVVn-TT0LKn"),
    ("064_Jesus_Crucified_Again.pdf", "1y493H_vF0Qn5hp8IiORJYIu4Q19ZXsqt"),
    (
        "063_Isan_No_Footprints_in_the_Blue_Sky.pdf",
        "1gmptVdXic5pZ592_lPrSeLcpk5E8v4vk",
    ),
    ("061_I_Say_Unto_You_Vol2.pdf", "1LaKwjBtR-ClMT0eEZyWxWMnLACq-eqmr"),
    ("060_I_Say_Unto_You_Vol1.pdf", "1rbGsFuC_GKXKn3oWzPCFikX9eDhezb2P"),
    ("059_I_Celebrate_Myself.pdf", "1EhNNqRl6JDWbRXpmObXJ0HTDyizu8XxN"),
    ("058_I_Am_the_Gate.pdf", "11dbu5JNexYLYJXYL1j1Y6MDc8BDUsl3S"),
    ("057_I_Am_That.pdf", "1_0lfMibS6LV6tIshHmbt82tr9-IlLuRI"),
    ("054_The_Hidden_Splendor.pdf", "1SiQVU4a4VdccvHHo3pFhYZH5CosSf5Za"),
    ("055_Hsin_Hsin_Ming.pdf", "15j5xkOSUIT5V3lL97Jck4fDddXS8YGzh"),
    ("053_The_Hidden_Harmony.pdf", "1ppH7e_kx8z1bLUT2MLAVhY8_kNsciFdP"),
    ("056_Hyakujo_The_Everest_of_Zen.pdf", "1MPYguVBhcSZT611_rMslqKbCTSO-yERS"),
    ("052_The_Heart_Sutra.pdf", "1YirUnYwdr-hYomls9zgMFZESnc0fGWPG"),
    ("048_The_Great_Zen_Master_Ta_Hui.pdf", "1LoS71wt2XBL7C_ZbHM7Sq4tuMhB7163d"),
    ("051_Hari_Om_Tat_Sat.pdf", "1pAAaebq6SkIZmS6sKwP3kQxP3Juxe0z8"),
    ("050_Guida_Spirituale.pdf", "1pwz8-4nr4AgIR60LY8Zy0aaP5G_qNKvt"),
    ("049_The_Guest.pdf", "1KU3jlGktEFge4U4Q8-RZbTHkdWIWlv-U"),
    (
        "047_The_Great_Pilgrimage_From_Here_to_Here.pdf",
        "1fK_uUVxQwDWWinZybXO0YKLWIPYkksQb",
    ),
    ("044_The_Golden_Future.pdf", "1Q_ErBc28ZYKd-rVOGPVPRaJweZDpcBZu"),
    ("045_The_Goose_is_Out.pdf", "1zgVP-CGdk5jKKlC1lezUAReLj3-Fpl4T"),
    ("046_The_Grass_Grown_By_Itself.pdf", "1UIVm5iKvlhtofhz3HRe3fNuysEI8reN1"),
    ("042_From_the_False_to_the_Truth.pdf", "1Q-JdfFoMoYiidodOKIzo98DcaHWt38Rt"),
    ("043_God_is_Dead.pdf", "1jDxY-W2lTKdqEp4HeIu0RpkC4NyhZHRT"),
    (
        "041_From_Unconciousness_to_Consciousness.pdf",
        "1H0xXJLZRbSDmLtifxjlAs9wetdFbJLlL",
    ),
    ("040_From_Personality_To_Individuality.pdf", "1H930DrYMrr4qJ3v3lJgFXBn3DzcJlpgv",),
    ("038_From_Ignorance_to_Innocence.pdf", "1aOq17mNB-x4tUUKnyxB6qDJKTDr8AE_E"),
    ("037_From_Death_to_Deathlessness.pdf", "1KRlwGPwF13r-Q0LKDGRW_4reKa82IvPl"),
    ("039_From_Misery_to_Enlightenment.pdf", "1LUZBovacDAA-KKlq9DMhq5V719s4jYfJ"),
    ("036_From_Darkness_to_Light.pdf", "1tu6UDbBkgLLqXfsDFY16wmgOZ1xYOkHx"),
    (
        "034_The_Fish_in_the_Sea_is_Not_Thirsty.pdf",
        "1TrN5DBHjqSHE8EzqF1813QzkCKKu2AIZ",
    ),
    ("035_From_Bondage_to_Freedom.pdf", "1Ubqbrzu71FGfCQ_Rj1ZdH-AvkasQkwyz"),
    ("032_The_Empty_Boat.pdf", "1uldABXAGlcym3VT_-67UZ7dfdF1GT9bC"),
    ("033_The_First_Principle.pdf", "15mfOceFFVfsTx-p03wQ9Ur4AhaObPsv4"),
    ("031_Ecstasy_The_Forgotten_Language.pdf", "1wdRDu1AjWF0jqVAYlaYj3TDaDc_mjaZx"),
    (
        "028_The_Discipline_of_Transcendence_Vol_4.pdf",
        "1LltVrZqRhkZrK9LZqG80wKtsjUEoJnMG",
    ),
    ("030_Dogen_the_Zen_Master.pdf", "1neeAI5jbYbXr37GF_3LHUqUqgVt4GtCB"),
    ("029_The_Divine_Melody.pdf", "1NAYgmQVgNZVhpZ7fTAHMWsn92XKS8LgI"),
    (
        "026_The_Discipline_of_Transcendence_Vol_2.pdf",
        "12ZcAocRSpjRInUnJcmS-qfRjw4HXtX_U",
    ),
    (
        "027_The_Discipline_of_Transcendence_Vol_3.pdf",
        "1c7tIdMWw1P6CjqRpf_a1QXdhQeHz4nPH",
    ),
    (
        "025_The_Discipline_of_Transcendence_Vol_1.pdf",
        "1adsF1HmcEDHJYMyB2fWbBdLy0zDBEO_P",
    ),
    ("024_The_Diamond_Sutra.pdf", "1HiDCEdrsgyQsLb8DJaJOGhKpuFL_Gyll"),
    ("022_Dang_Dang_Doko_Dang.pdf", "1CPmFIR50VaZMANZku4npGLNDEwloS0l_"),
    ("021_Communism_and_Zen_Fire.pdf", "1jC-qNiWr6IO62xt5Sfho9Myr1AUlwQBA"),
    ("019_Come_Follow_To_You_Vol4.pdf", "1ZeYsy47PIlzWFZXHEChf0gVxkGuYrgWj"),
    ("020_Come_Come_Yet_Again_Come.pdf", "1ZnniPtqaQ4oZnTDdTyjlFuO9984ERRGz"),
    ("017_Come_Follow_To_You_Vol2.pdf", "1qoszFa4zFisaX3Ng_p5Gn7RLt45nkyMc"),
    ("018_Come_Follow_To_You_Vol3.pdf", "15c2pDaM1RSS5-T6hQI-Bbq_5E_gPfhTl"),
    ("015_Christianity_The_Deadliest_Poison.pdf", "163mnzKFp9yVAdOX1lFNeRAewygeIDD58",),
    ("016_Come_Follow_To_You_Vol1.pdf", "1QB0FJ-RuDrPd3imqHGI7PQT5TmVBIg5v"),
    ("013_The_Book_of_Wisdom.pdf", "1F6SSsxV7FEw8-RTQbSIEotaaX1VrjXpY"),
    ("011_Beyond_Psychology.pdf", "1TwTG7DkwlnDcZ3kd5xma9UzKpNkJ7iOF"),
    (
        "014_The_Buddha_The_Emptiness_of_the_Heart.pdf",
        "1bO33tjlsES5emOQu_8voLHa4F9F7o9sJ",
    ),
    ("012_Bodhidharma.pdf", "1CzUtdUXUduOtiXy0iZqwgCI-gyzc4X8_"),
    ("010_Beyond_Enlightenment.pdf", "180x9lTRcK0bhFMN_hnnqY2rz0Bd7z-Ou"),
    ("009_The_Beloved_Vol_2.pdf", "1rldZu_EWkHxdRh4z82btF8R8j5wKUCqF"),
    ("007_Be_Still_and_Know.pdf", "16dYxkE-OTADL0pEve6du6OOdX_xqClvI"),
    ("008_The_Beloved_Vol_1.pdf", "1VXk5PiZkRchMpr4cLy0iTkoHjedDC71y"),
    ("006_The_Art_of_Dying.pdf", "1E1SSJzOu8ZVhSPiqO0tDUKm-I87PjOxQ"),
    ("005_And_The_Flowers_Showered.pdf", "1Urj-5-tIalf3oa7HRkNnd9NlLnowg36b"),
    ("004_A_Bird_on_the_Wing.pdf", "1e9nf6CMg3FrbUF-VnkR66yc5Z-1tHB4b"),
    ("003_Ancient_Music_in_the_Pines.pdf", "1G6jVYssReABCxkmQG5135L3WysO6ce09"),
    ("002_Ah_This.pdf", "1MpaOnlJro0R7BgY7hC2Dz4nNylPTsKnX"),
    ("001_A_Sudden_Clash_of_Thunder.pdf", "1Da6LPnEvLkpT_GE-fEZHv8HBz_WOBGj7"),
]


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1250" height="720" type="application/pdf">'
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1350" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# Python code to convert into dictionary
def tuple_to_dict(tup, di):
    di = dict(tup)
    return di


def callback_delete():
    first_pdf_path = Path("data/001_A_Sudden_Clash_of_Thunder.pdf")
    first_pdf_path = str(first_pdf_path)
    all_files = Path("data/").glob("*.pdf")
    for f in all_files:
        if str(f) == first_pdf_path:
            pass
        else:
            try:
                f.unlink()
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))


def set_page_title(title):
    st.sidebar.markdown(
        unsafe_allow_html=True,
        body=f"""
        <iframe height=0 srcdoc="<script>
            const title = window.parent.document.querySelector('title') \

            const oldObserver = window.parent.titleObserver
            if (oldObserver) {{
                oldObserver.disconnect()
            }} \

            const newObserver = new MutationObserver(function(mutations) {{
                const target = mutations[0].target
                if (target.text !== '{title}') {{
                    target.text = '{title}'
                }}
            }}) \

            newObserver.observe(title, {{ childList: true }})
            window.parent.titleObserver = newObserver \

            title.text = '{title}'
        </script>" />
    """,
    )


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    set_page_title("Osho Books")
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    dictionary = {}
    pdf_name = [i[0] for i in pdf_list]
    pdf_name.reverse()
    pdf_mapping = tuple_to_dict(pdf_list, dictionary)
    Path("data/").mkdir(parents=True, exist_ok=True)
    value = st.sidebar.selectbox("Select a Book", pdf_name, on_change=callback_delete())
    text = value.split(".")[0].split("_")[1:]
    text = " ".join(text)
    st.header(f"{text}, Osho")
    if not Path(f"data/{value}").is_file():
        download_file_from_google_drive(pdf_mapping[value], f"data/{value}")
    time.sleep(0.1)
    show_pdf(f"data/{value}")
    st.markdown("""---""")
