
#include <fstream>
#include <iostream>
#include <vector>

#include <chrono>
#include <thread>

#include "bgen.h"
#include "header.h"
#include "samples.h"
#include "variant.h"

int main() {
  std::string path = "/illumina/scratch/deep_learning/pfiziev/ukbiobank/data/array_genotypes/ukb_imp_chr21_v3.bgen";
  bgen::Bgen bgen_file(path);
  
  // auto rsids = bgen_file.rsids();
  // std::vector<int> to_drop = {0, 1};
  // bgen_file.drop_variants(to_drop);
  //
  // auto var = bgen_file[20000];
  // std::cout << var.chrom << ":" << var.pos << "\n";
  
  int i = 0;
  for (auto var : bgen_file.variants) {
    i++;
    std::cout << var.rsid << " " << i << "\n";
    auto time_a = std::chrono::high_resolution_clock::now();
    // auto geno = var.probabilities();
    auto time_b = std::chrono::high_resolution_clock::now();
    auto minor_allele_dosage = var.minor_allele_dosage();
    auto time_c = std::chrono::high_resolution_clock::now();
    // std::cout << " - parse genotypes: " << std::chrono::duration_cast<std::chrono::milliseconds>(time_b - time_a).count() << std::endl;
    std::cout << " - get alt dosage: " << std::chrono::duration_cast<std::chrono::milliseconds>(time_c - time_b).count() << std::endl;
    // std::cout << " - dosage size: " << alt_dosage.size() << std::endl;
    
    // double total = 0;
    // for (auto d : minor_allele_dosage) {
    //   total += d;
    // }
    // double mean_dosage = total / (double) minor_allele_dosage.size();
    // std::cout << " - dosage mean: " << mean_dosage << std::endl;
    
    // for (auto d : minor_allele_dosage ) {
    //   std::cout << d << "\n";
    // }
    // break;
  }
  
  std::cout << bgen_file.variants.size() << std::endl;
  std::cout << "sleeping after parsing file" << std::endl;
  std::this_thread::sleep_for(std::chrono::seconds(20));
}
