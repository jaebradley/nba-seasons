from enum import Enum, auto
class Season(Enum):
    _1949 = (auto(), 1949)
    _1950 = (auto(), 1950)
    _1951 = (auto(), 1951)
    _1952 = (auto(), 1952)
    _1953 = (auto(), 1953)
    _1954 = (auto(), 1954)
    _1955 = (auto(), 1955)
    _1956 = (auto(), 1956)
    _1957 = (auto(), 1957)
    _1958 = (auto(), 1958)
    _1959 = (auto(), 1959)
    _1960 = (auto(), 1960)
    _1961 = (auto(), 1961)
    _1962 = (auto(), 1962)
    _1963 = (auto(), 1963)
    _1964 = (auto(), 1964)
    _1965 = (auto(), 1965)
    _1966 = (auto(), 1966)
    _1967 = (auto(), 1967)
    _1968 = (auto(), 1968)
    _1969 = (auto(), 1969)
    _1970 = (auto(), 1970)
    _1971 = (auto(), 1971)
    _1972 = (auto(), 1972)
    _1973 = (auto(), 1973)
    _1974 = (auto(), 1974)
    _1975 = (auto(), 1975)
    _1976 = (auto(), 1976)
    _1977 = (auto(), 1977)
    _1978 = (auto(), 1978)
    _1979 = (auto(), 1979)
    _1980 = (auto(), 1980)
    _1981 = (auto(), 1981)
    _1982 = (auto(), 1982)
    _1983 = (auto(), 1983)
    _1984 = (auto(), 1984)
    _1985 = (auto(), 1985)
    _1986 = (auto(), 1986)
    _1987 = (auto(), 1987)
    _1988 = (auto(), 1988)
    _1989 = (auto(), 1989)
    _1990 = (auto(), 1990)
    _1991 = (auto(), 1991)
    _1992 = (auto(), 1992)
    _1993 = (auto(), 1993)
    _1994 = (auto(), 1994)
    _1995 = (auto(), 1995)
    _1996 = (auto(), 1996)
    _1997 = (auto(), 1997)
    _1998 = (auto(), 1998)
    _1999 = (auto(), 1999)
    _2000 = (auto(), 2000)
    _2001 = (auto(), 2001)
    _2002 = (auto(), 2002)
    _2003 = (auto(), 2003)
    _2004 = (auto(), 2004)
    _2005 = (auto(), 2005)
    _2006 = (auto(), 2006)
    _2007 = (auto(), 2007)
    _2008 = (auto(), 2008)
    _2009 = (auto(), 2009)
    _2010 = (auto(), 2010)
    _2011 = (auto(), 2011)
    _2012 = (auto(), 2012)
    _2013 = (auto(), 2013)
    _2014 = (auto(), 2014)
    _2015 = (auto(), 2015)
    _2016 = (auto(), 2016)
    _2017 = (auto(), 2017)
    _2018 = (auto(), 2018)
    _2019 = (auto(), 2019)
    _2020 = (auto(), 2020)
    _2021 = (auto(), 2021)
    _2022 = (auto(), 2022)

    def __init__(self, value, start_year):
        self._value_ = value
        self._start_year_ = start_year

    @property
    def start_year(self):
        return self._start_year_

    def __lt__(self, other):
        return self.start_year < other.start_year

    def __gt__(self, other):
        return self.start_year > other.start_year

    def __str__(self) -> str:
        return self.name
            