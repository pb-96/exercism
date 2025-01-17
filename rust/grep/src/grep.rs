use anyhow::Error;
use std::fs;

/// While using `&[&str]` to handle flags is convenient for exercise purposes,
/// and resembles the output of [`std::env::args`], in real-world projects it is
/// both more convenient and more idiomatic to contain runtime configuration in
/// a dedicated struct. Therefore, we suggest that you do so in this exercise.
///
/// In the real world, it's common to use crates such as [`clap`] or
/// [`structopt`] to handle argument parsing, and of course doing so is
/// permitted in this exercise as well, though it may be somewhat overkill.
///
/// [`clap`]: https://crates.io/crates/clap
/// [`std::env::args`]: https://doc.rust-lang.org/std/env/fn.args.html
/// [`structopt`]: https://crates.io/crates/structopt
#[derive(Debug, Default)]
pub struct Flags {
    n: bool,
    l: bool,
    i: bool,
    v: bool,
    x: bool,
}

impl Flags {
    pub fn new(flags: &[&str]) -> Self {
        let mut flags_object = Self::default();
        for flag in flags {
            match *flag {
                "-n" => flags_object.n = true,
                "-l" => flags_object.l = true,
                "-i" => flags_object.i = true,
                "-v" => flags_object.v = true,
                "-x" => flags_object.x = true,
                _ => {
                    println!("Unrecognized flag: {}", flag);
                }
            }
        }
        flags_object
    }
}

fn match_line(pattern: &str, line: &String, flags: &Flags) -> bool {
    let compare_on = pattern.to_string();
    return {
        match (flags.x, flags.i) {
            (true, true) => line.to_lowercase() == pattern.to_lowercase(),
            (true, false) => line == pattern,
            (false, true) => line.to_lowercase().contains(&pattern.to_lowercase()),
            (false, false) => line.contains(&pattern),
        }
    }
}

fn read_lines_from_file(filename: &str, flags: &Flags, pattern: &str, multiple: bool) -> Result<Vec<String>, Error> {
    let raw_content: String = fs::read_to_string(filename)?;
    let string_file = filename.to_string();
    let mut lines = Vec::new();

    for (_index, line) in raw_content.split("\n").enumerate() {
        let mut string_line = String::from(line.to_string());
        if string_line.is_empty() {
            continue 
        }

        let matched = match_line(pattern, &string_line, flags);
        if (matched && flags.v) || (!matched && !flags.v) {
            continue;
        }
        
        if flags.l {
            lines.push(string_file.clone());
            return Ok(lines);
        } else if flags.n {
            let increment_copy = _index + 1;
            string_line = format!("{increment_copy}:{string_line}");
        }

        if multiple {
            string_line = format!("{string_file}:{string_line}");
        }
        lines.push(string_line);
    }
    
    Ok(lines)
}

pub fn grep(pattern: &str, flags: &Flags, files: &[&str]) -> Result<Vec<String>, Error> {
    let mut found_data: Vec<String> = Vec::new();
    let multiple = files.len() > 1;
    for f in files {
        let mut raw = read_lines_from_file(f, flags, pattern, multiple);
        let mut data = match raw {
            Ok(raw) => raw,
            Err(e) => return Err(e)
        };
        found_data.append(&mut data);
    }
    Ok(found_data)
}


