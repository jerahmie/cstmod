// =============================================================================
// cst_find_exports
// =============================================================================

use std::path::*;
use std::io;
use std::fs::{self, ReadDir};
use glob::glob_with;
use glob::MatchOptions;

/// cst_find_exports 
/// returns a sorted vector of files that matches the given pattern/// 
pub fn cst_find_exports(path: PathBuf) -> io::Result<Vec<PathBuf>> {
    let mut entries =  fs::read_dir(path)?
        .map(|res| res.map(|e| e.path()))
        .collect::<Result<Vec<_>, io::Error>>()?;
    entries.sort();

    Ok(entries)
}
pub fn cst_find_exports_glob(path: &str) -> io::Result<Vec<PathBuf>> {
    let options = MatchOptions{
            case_sensitive: false,
            require_literal_separator: false,
            require_literal_leading_dot: false,
    };
    let mut entries = Vec::new();
    for result in glob_with(path, options).expect("Glob failed") {
        match result {
            Ok(p)  => entries.push(p),
            Err(e) => println!("{:>}", e),
        }
    }

    Ok(entries)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_cst_find_exports() {
        let path = PathBuf::from(r"../../../test_data/");
        let found_exports = cst_find_exports(path).unwrap();
        assert_eq!(cst_find_exports(PathBuf::from(".")).unwrap().len(), 2);
        assert_eq!(found_exports[0], PathBuf::from(r"../../../test_data/README.md"));
    }
    #[test]
    fn test_find_exports_glob() {
        let path = "../../../test_data/*";
        println!("path: {}", path);
        let found_exports = cst_find_exports_glob(path).unwrap();
        assert_eq!(found_exports[0], PathBuf::from(r"../../../test_data/README.md"))
    }
}