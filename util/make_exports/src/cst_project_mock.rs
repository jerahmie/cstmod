// ----------------------------------------------------------------------------
// cst_project_mock.rs
// ----------------------------------------------------------------------------
use std::path::*;
use std::fs;
use std::io;

pub fn cst_project_mock(path: &PathBuf, project_name: &str) -> io::Result<()> {
    let mut cst_project_dir = path.to_owned();
    cst_project_dir.push(PathBuf::from(project_name));

    // Create a file representing the main CST project file
    let mut cst_project_name = PathBuf::from(&cst_project_dir);
    cst_project_name.set_extension("cst");
    let _file = fs::File::create(&cst_project_name)
        .expect("Error encountered while creating file!");

    // Create a directory representing the CST data filess
    cst_project_dir.push(PathBuf::from(r"Export/3d"));
    fs::create_dir_all(&cst_project_dir)
        .expect("Error encountered while creating project directory");    
    
    Ok(())
}

// construct a 3d name for a given field/frequency/label format.
fn field_data3_export_name(args: &[&str]) -> String {
    let mut field_name = String::new();
    if args.len() != 4 {
        panic!("Field arguments contains wrong number of values.");
    }
    // This could probably be replaced by a partial function
    field_name.push_str(args[0]);
    field_name.push_str(" (f=");
    field_name.push_str(args[1]);
    field_name.push_str(") [");
    field_name.push_str(args[2]);
    field_name.push_str(args[3]);
    field_name.push_str("].h5");
    return field_name;
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_cst_project_mock() {
        let mut path = PathBuf::from("../../../test_data/");
        let project_name = "test";
        let result = cst_project_mock(&path, project_name);
        path.push(project_name);
        assert_eq!(result.unwrap(), ());
    }
    
    #[test]
    fn test_field_data3_export_name() {
        let field_str = ["e-field", "447", "AC", "1"];
        let field_name = field_data3_export_name(&field_str);
        assert_eq!(field_name, "e-field (f=447) [AC1].h5");
    }
}