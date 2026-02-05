let vowels = 'aeiouy';
let consonants = 'bcdfghklmnprstvzx';

let encode = function(input, encoding) {
  if (!Buffer.isBuffer(input)) {
    input = new Buffer(input, encoding);
  }

  let result = 'x',
      checksum = 1,
      len = input.length,
      byte1, byte2,
      d, e, i;

  // create full tuples
  for (i = 0; i + 1 < len; i += 2) {
    byte1 = input.readUInt8(i);
    result += odd_partial(byte1, checksum);

    byte2 = input.readUInt8(i + 1);
    d = (byte2 >> 4) & 15;
    e = byte2 & 15;

    result += consonants.charAt(d) + '-' + consonants.charAt(e);

    checksum = next_checksum(checksum, byte1, byte2);
  }

  // handle partial tuple
  if (i < len) {
    byte1 = input.readUInt8(i);
    result += odd_partial(byte1, checksum);
  } else {
    result += even_partial(checksum);
  }

  result += 'x';
  return result;
};

let odd_partial = function(raw_byte, checksum) {
  let a = (((raw_byte >> 6) & 3) + checksum) % 6,
      b = (raw_byte >> 2) & 15,
      c = ((raw_byte & 3) + Math.floor(checksum / 6)) % 6;

  return vowels.charAt(a) + consonants.charAt(b) + vowels.charAt(c);
}

let even_partial = function(checksum) {
  let a = checksum % 6,
      b = 16,
      c = Math.floor(checksum / 6);

  return vowels.charAt(a) + consonants.charAt(b) + vowels.charAt(c);
};

let decode = function(input) {
  if (input.substr(0, 1) !== 'x' ||
      input.substr(-1, 1) !== 'x') {
    throw new Error('Corrupt string');
  }

  let ascii_tuples = input.substring(1, input.length - 1).match(/.{3,6}/g),
      len = ascii_tuples ? ascii_tuples.length : 0,
      char_codes = [],
      checksum = 1,
      byte1, byte2, i,
      tuple;

  // handle full tuples
  for (i = 0; i < len - 1; ++i) {
    tuple = decode_tuple(ascii_tuples[i]);

    byte1 = decode_3part_byte(tuple[0], tuple[1], tuple[2], checksum);
    byte2 = decode_2part_byte(tuple[3], tuple[4]);

    checksum = next_checksum(checksum, byte1, byte2);

    char_codes.push(byte1);
    char_codes.push(byte2);
  }

  // handle partial tuple
  tuple = decode_tuple(ascii_tuples[len - 1]);
  if (tuple[1] === 16) {
    if (tuple[0] !== checksum % 6 ||
        tuple[2] !== Math.floor(checksum / 6)) {
      throw new Error('Corrupt string');
    }
  } else {
    byte1 = decode_3part_byte(tuple[0], tuple[1], tuple[2], checksum);
    char_codes.push(byte1);
  }

  return new Buffer(char_codes);
};

let decode_tuple = function(ascii_tuple) {
  return [
    vowels.indexOf(ascii_tuple[0]),
    consonants.indexOf(ascii_tuple[1]),
    vowels.indexOf(ascii_tuple[2]),
    consonants.indexOf(ascii_tuple[3]),
    consonants.indexOf(ascii_tuple[5]),
  ];
};

let decode_3part_byte = function(a, b, c, checksum) {
  let high = (a - (checksum % 6) + 6) % 6,
      mid = b,
      low = (c - (Math.floor(checksum / 6) % 6) + 6) % 6;

  if (high >= 4 || low >= 4) {
    throw new Error('Corrupt string');
  }

  return (high << 6) | (mid << 2) | low;
};

let decode_2part_byte = function(d, e) {
  return (d << 4) | e;
}

let next_checksum = function(checksum, byte1, byte2) {
  return ((checksum * 5) + (byte1 * 7) + byte2) % 36;
}

export let babble_decode = (msg) => {
  console.log(decode(msg).toString())
}