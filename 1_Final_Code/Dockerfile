# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/minimal-notebook

MAINTAINER Mohit Mittal <mittal.mo@husky.neu.edu>

USER root

# libav-tools for matplotlib anim
RUN apt-get update && \
    apt-get clean && \
            rm -rf /var/lib/apt/lists/*

	    USER $NB_USER
	        
		# Install Python 3 packages
		# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
		# use notebook-friendly backends in these images
		RUN conda install --quiet --yes \
		    'nomkl' \
		            'ipywidgets=5.2*' \
			        'pandas=0.19*' \
				        'numexpr=2.6*' \
					    'matplotlib=1.5*' \
					            'scipy=0.17*' \
						        'beautifulsoup4=4.5.*' \
							    'lxml' \
								'html5lib' \
								    'boto' \
								       'luigi' \
								          'mechanicalsoup' \
								                    'xlrd'  && \
					                              conda remove --quiet --yes --force qt pyqt && \
						                      conda clean -tipsy
									
								      	ADD Classes Classes
									ADD part1.py part1.py
									ADD part2.py part2.py
									ADD Classification_Forest_Random.R Classification_Forest_Random.R
									ADD Classification_Logistic_Regression.R Classification_Logistic_Regression.R
									ADD neuralnet.R neuralnet.R
									ADD 
									
										
									EXPOSE 8123		
									CMD ["python3","part1.py", "Summarize_data", "--local-scheduler"]
								      	


