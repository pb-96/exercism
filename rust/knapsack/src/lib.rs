// use itertools::Itertools; // Import the Itertools trait

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct Item {
    pub weight: u32,
    pub value: u32,
}


pub fn combine_items(items: &[Item]) -> Vec<Vec<usize>> {
    let n = items.len();
    let mut combinations = Vec::new();
    let mut last_iter = combinations.clone();
    // Generate all combinations using bitmasks (1 to 2^n - 1)
    for mask in 1..(1 << n) {
        let mut combination = Vec::new();
        for idx in 0..n {
            if mask & (1 << idx) != 0 {
                combination.push(idx);
            }
        }
        combinations.push(combination);
    }

    combinations
}


pub fn maximum_value(max_weight: u32, items: &[Item]) -> u32 {
    let mut max_total: u32 = 0;
    for idx_combs in combine_items(items) {
        let mut _items: Vec<Item> = Vec::new();
        for idx in idx_combs.iter() {
            _items.push(items[*idx].clone())
        }
        let this_weight: i32 = items.iter().map(|item| item.weight as i32).sum();
        let this_val: i32 = items.iter().map(|item| item.value as i32).sum();

        if this_weight <= max_weight.try_into().unwrap() && this_val > max_total.try_into().unwrap() {
            max_total = this_val.try_into().unwrap();
            
        }
    }

    max_total
}
