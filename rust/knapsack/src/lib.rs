
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct Item {
    pub weight: u32,
    pub value: u32,
}

pub fn maximum_value(max_weight: u32, items: &[Item]) -> u32 {
    let mut dp = vec![0; (max_weight + 1) as usize];

    for item in items {
        for w in (item.weight as usize..=max_weight as usize).rev() {
            dp[w] = dp[w].max(dp[w - item.weight as usize] + item.value);
        }
    }

    dp[max_weight as usize]
}
