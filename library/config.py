from library import igfunc

# Current time in Hongkong
now_utc = igfunc.datetime.datetime.now(igfunc.pytz.timezone('Asia/Hong_Kong'))

# Ubah Bagian Ini
countTarget = '100' # Ambil jumlah akun per target
cookieFile = 'cookieData.txt' # File cookie
targetFile = 'targetData.txt' # File target