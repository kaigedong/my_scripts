1. Two Sum

  ``` rust
  use std::collections::HashMap;
  impl Solution {
      pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
      
      let mut tmp_set = HashMap::new(); // 创建一个可扩容的Hash表

      for (i,j) in nums.iter().enumerate() { // 对列表迭代的方法
          if tmp_set.contains_key(&(target - j)) { //判断Hash表是否包含特定key
              return vec![*(tmp_set.get(&(target-j)).unwrap()), i as i32] //显式类型转换，Hash表.get 取值
          } else {
              tmp_set.insert(j, i as i32); // Hash表扩容
          }
      };
      vec![0,0]
      }
  }
  ```

7. Reverse Integer

  ``` rust
  impl Solution {
      pub fn reverse(x: i32) -> i32 {

          let mut out = String::new();

          if x > 0 {
              for c in x.to_string().chars().rev() { // 数字转字符串、字符串迭代方法
                  out.push(c); // 字符串扩充char
              }
              match out.parse::<i32>() { // 错误处理
                  Ok(out) => {return out;},
                  _ => {return 0;}
              }
          } else {
              let x = -1 * x;
              for c in x.to_string().chars().rev() {
                  out.push(c);
              }

              match out.parse::<i32>() {
                  Ok(out) => {return -1 * out;},
                  _ => {return 0;}
              }
          }
      }
  }
```
