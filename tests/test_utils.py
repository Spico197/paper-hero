import re


def test_parse_bib():
    string = """@proceedings{wsc-2023-sanskrit,
    title = "Proceedings of the Computational Sanskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    editor = "Kulkarni, Amba  and
      Hellwig, Oliver",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.0",
}
@inproceedings{krishna-etal-2023-neural,
    title = "Neural Approaches for Data Driven Dependency Parsing in {S}anskrit",
    author = "Krishna, Amrith  and
      Gupta, Ashim  and
      Garasangi, Deepak  and
      Sandhan, Jeevnesh  and
      Satuluri, Pavankumar  and
      Goyal, Pawan",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.1",
    pages = "1--20",
}
@inproceedings{sandhan-etal-2023-evaluating,
    title = "Evaluating Neural Word Embeddings for {S}anskrit",
    author = "Sandhan, Jivnesh  and
      Paranjay, Om Adideva  and
      Digumarthi, Komal  and
      Behra, Laxmidhar  and
      Goyal, Pawan",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.2",
    pages = "21--37",
}
@inproceedings{sriram-etal-2023-validation,
    title = "Validation and Normalization of {DCS} corpus and Development of the {S}anskrit Heritage Engine{'}s Segmenter",
    author = "Sriram, Krishnan  and
      Kulkarni, Amba  and
      Huet, G{\'e}rard",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.3",
    pages = "38--58",
}
@inproceedings{sarkar-etal-2023-pre,
    title = "Pre-annotation Based Approach for Development of a {S}anskrit Named Entity Recognition Dataset",
    author = "Sujoy, Sarkar  and
      Krishna, Amrith  and
      Goyal, Pawan",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.4",
    pages = "59--70",
}
@inproceedings{maity-etal-2023-disambiguation,
    title = "Disambiguation of Instrumental, Dative and Ablative Case suffixes in {S}anskrit",
    author = "Maity, Malay  and
      Panchal, Sanjeev  and
      Kulkarni, Amba",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.5",
    pages = "71--88",
}
@inproceedings{mahesh-bhattacharya-2023-creation,
    title = "Creation of a Digital Rig {V}edic Index (Anukramani) for Computational Linguistic Tasks",
    author = "Mahesh, A V S D S  and
      Bhattacharya, Arnab",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.6",
    pages = "89--96",
}
@inproceedings{neill-2023-skrutable,
    title = "Skrutable: Another Step Toward Effective {S}anskrit Meter Identification",
    author = "Neill, Tyler",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.7",
    pages = "97--112",
}
@inproceedings{terdalkar-bhattacharya-2023-chandojnanam,
    title = "Chandojnanam: A {S}anskrit Meter Identification and Utilization System",
    author = "Terdalkar, Hrishikesh  and
      Bhattacharya, Arnab",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.8",
    pages = "113--127",
}
@inproceedings{ajotikar-scharf-2023-development,
    title = "Development of a {TEI} standard for digital {S}anskrit texts containing commentaries: A pilot study of Bhaṭṭti{'}s R{=a}vaṇavadha with Mallin{=a}tha{'}s commentary on the first canto",
    author = "Ajotikar, Tanuja P  and
      Scharf, Peter M",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.9",
    pages = "128--145",
}
@inproceedings{scharf-chauhan-2023-ramopakhyana,
    title = "R{=a}mop{=a}khy{=a}na: A Web-based reader and index",
    author = "Scharf, Peter M  and
      Chauhan, Dhruv",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.10",
    pages = "146--154",
}
@inproceedings{terdalkar-etal-2023-semantic,
    title = "Semantic Annotation and Querying Framework based on Semi-structured Ayurvedic Text",
    author = "Terdalkar, Hrishikesh  and
      Bhattacharya, Arnab  and
      Dubey, Madhulika  and
      Ramamurthy, S  and
      Singh, Bhavna Naneria",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.11",
    pages = "155--173",
}
@inproceedings{susarla-etal-2023-shaastra,
    title = "Shaastra Maps: Enabling Conceptual Exploration of {I}ndic Shaastra Texts",
    author = "Susarla, Sai  and
      Jammalamadaka, Suryanarayana  and
      Nishankar, Vaishnavi  and
      Panuganti, Siva  and
      Ryali, Anupama  and
      Sushrutha, S",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.12",
    pages = "174--187",
}
@inproceedings{hellwig-etal-2023-vedic,
    title = "The {V}edic corpus as a graph. An updated version of Bloomfields {V}edic Concordance",
    author = "Hellwig, Oliver  and
      Sellmer, Sven  and
      Amano, Kyoko",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.13",
    pages = "188--200",
}
@inproceedings{harnsukworapanich-supphipat-2023-transmission,
    title = "The transmission of the Buddha{'}s teachings in the digital age",
    author = "Harnsukworapanich, Sumachaya  and
      Supphipat, Phatchareporn",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.14",
    pages = "201--212",
}
@inproceedings{zigmond-2023-distinguishing,
    title = "Distinguishing Commentary from Canon: Experiments in P{=a}li Computational Linguistics",
    author = "Zigmond, Dan",
    booktitle = "Proceedings of the Computational {S}anskrit & Digital Humanities: Selected papers presented at the 18th World {S}anskrit Conference",
    month = jan,
    year = "2023",
    address = "Canberra, Australia (Online mode)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.wsc-csdh.15",
    pages = "213--222",
}"""  # noqa: W605
    new_string = re.sub(r"and$\n\s+", "and  ", string, flags=re.MULTILINE)
    print(new_string)


if __name__ == "__main__":
    test_parse_bib()
