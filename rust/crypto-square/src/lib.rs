pub fn encrypt(input: &str) -> String {
    let pain = input
        .chars()
        .filter_map(|c| Some(c.to_ascii_lowercase()).filter(char::is_ascii_alphanumeric))
        .collect::<Vec<_>>();

    let width = (pain.len() as f64).sqrt().ceil() as usize;

    (0..width)
        .map(|i| {
            pain.chunks(width)
                .filter_map(|v| v.get(i).or(Some(&' ')))
                .collect::<String>()
        })
        .collect::<Vec<_>>()
        .join(" ")
}
