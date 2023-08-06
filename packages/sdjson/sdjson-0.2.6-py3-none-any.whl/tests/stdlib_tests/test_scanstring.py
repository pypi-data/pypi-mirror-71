# stdlib
# These tests test the internals of json, so we really do
#  mean to be importing json here
# stdlib
import json
import sys

# 3rd party
import pytest  # type: ignore

# this package
import sdjson


def test_scanstring():
	scanstring = json.decoder.scanstring
	assert scanstring('"z\U0001d120x"', 1, True) == ('z\U0001d120x', 5)

	assert scanstring('"\\u007b"', 1, True) == ('{', 8)

	assert scanstring('"A JSON payload should be an object or array, not a string."', 1,
						True) == ('A JSON payload should be an object or array, not a string.', 60)

	assert scanstring('["Unclosed array"', 2, True) == ('Unclosed array', 17)

	assert scanstring('["extra comma",]', 2, True) == ('extra comma', 14)

	assert scanstring('["double extra comma",,]', 2, True) == ('double extra comma', 21)

	assert scanstring('["Comma after the close"],', 2, True) == ('Comma after the close', 24)

	assert scanstring('["Extra close"]]', 2, True) == ('Extra close', 14)

	assert scanstring('{"Extra comma": true,}', 2, True) == ('Extra comma', 14)

	assert scanstring('{"Extra value after close": true} "misplaced quoted value"', 2,
						True) == ('Extra value after close', 26)

	assert scanstring('{"Illegal expression": 1 + 2}', 2, True) == ('Illegal expression', 21)

	assert scanstring('{"Illegal invocation": alert()}', 2, True) == ('Illegal invocation', 21)

	assert scanstring('{"Numbers cannot have leading zeroes": 013}', 2,
						True) == ('Numbers cannot have leading zeroes', 37)

	assert scanstring('{"Numbers cannot be hex": 0x14}', 2, True) == ('Numbers cannot be hex', 24)

	assert scanstring('[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]', 21, True) == ('Too deep', 30)

	assert scanstring('{"Missing colon" null}', 2, True) == ('Missing colon', 16)

	assert scanstring('{"Double colon":: null}', 2, True) == ('Double colon', 15)

	assert scanstring('{"Comma instead of colon", null}', 2, True) == ('Comma instead of colon', 25)

	assert scanstring('["Colon instead of comma": false]', 2, True) == ('Colon instead of comma', 25)

	assert scanstring('["Bad value", truth]', 2, True) == ('Bad value', 12)


def test_surrogates():
	scanstring = json.decoder.scanstring

	def assertScan(given, expect):
		assert scanstring(given, 1, True) == (expect, len(given))

	assertScan('"z\\ud834\\u0079x"', 'z\ud834yx')
	assertScan('"z\\ud834\\udd20x"', 'z\U0001d120x')
	assertScan('"z\\ud834\\ud834\\udd20x"', 'z\ud834\U0001d120x')
	assertScan('"z\\ud834x"', 'z\ud834x')
	assertScan('"z\\ud834\udd20x12345"', 'z\ud834\udd20x12345')
	assertScan('"z\\udd20x"', 'z\udd20x')
	assertScan('"z\ud834\udd20x"', 'z\ud834\udd20x')
	assertScan('"z\ud834\\udd20x"', 'z\ud834\udd20x')
	assertScan('"z\ud834x"', 'z\ud834x')


def test_bad_escapes():
	scanstring = json.decoder.scanstring
	bad_escapes = [
			'"\\"',
			'"\\x"',
			'"\\u"',
			'"\\u0"',
			'"\\u01"',
			'"\\u012"',
			'"\\uz012"',
			'"\\u0z12"',
			'"\\u01z2"',
			'"\\u012z"',
			'"\\u0x12"',
			'"\\u0X12"',
			'"\\ud834\\"',
			'"\\ud834\\u"',
			'"\\ud834\\ud"',
			'"\\ud834\\udd"',
			'"\\ud834\\udd2"',
			'"\\ud834\\uzdd2"',
			'"\\ud834\\udzd2"',
			'"\\ud834\\uddz2"',
			'"\\ud834\\udd2z"',
			'"\\ud834\\u0x20"',
			'"\\ud834\\u0X20"',
			]
	for s in bad_escapes:
		with pytest.raises(sdjson.JSONDecodeError):
			sys.stderr.write(str(s))
			sys.stderr.flush()
			scanstring(s, 1, True)


def test_overflow():
	with pytest.raises(OverflowError):
		json.decoder.scanstring(b"xxx", sys.maxsize + 1)
