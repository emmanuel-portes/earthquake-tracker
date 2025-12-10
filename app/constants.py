class Constants:
    MAG_TYPES: list[str] = ['md', 'ml', 'ms', 'mw', 'me', 'mi', 'mb', 'mlg']
    PER_PAGE_LIMIT: int = 1000
    MIN_LATITUDE, MAX_LATITUDE = [-90.0, 90.0]
    MIN_MAGNITUDE, MAX_MAGNITUDE = [-1.0, 10.0]
    MIN_LONGITUDE, MAX_LONGITUDE = [-180.0, 180.0]