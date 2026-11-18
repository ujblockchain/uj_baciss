package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
)

func main() {
	// directory you want to scan
	rootDir := "./" // change to your project folder

	// output file
	outFile := "output.txt"
	f, err := os.Create(outFile)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	// walk through directory
	err = filepath.Walk(rootDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			ext := filepath.Ext(path)
			switch ext {
			case ".ipynb", ".md", ".json", ".html", ".css", ".js", ".yml", ".xml", ".sum", ".mod":
				content, err := ioutil.ReadFile(path)
				if err != nil {
					return err
				}
				// write file path and content
				_, err = fmt.Fprintf(f, "=== %s ===\n%s\n\n", path, string(content))
				if err != nil {
					return err
				}
				fmt.Println("Added:", path)
			}
		}
		return nil
	})

	if err != nil {
		panic(err)
	}

	fmt.Println("Extraction completed! Output saved to", outFile)
}
