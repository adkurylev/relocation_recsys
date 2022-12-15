from sklearn.metrics.pairwise import cosine_similarity, cosine_distances, euclidean_distances, rbf_kernel, laplacian_kernel
import pandas as pd
import numpy as np
from sklearn import preprocessing

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from textwrap import wrap
import matplotlib.patches as mpl_patches


def get_similarity_matr(features):
    #computing normilized desired distances from given features
    cos_dis = cosine_distances(features, features)
    cos_dis = 1.0 - (cos_dis / np.max(cos_dis))

    rbf_ker = rbf_kernel(features, features)
    rbf_ker = rbf_ker / np.max(rbf_ker)

    lap_ker = laplacian_kernel(features, features)
    lap_ker = lap_ker / np.max(lap_ker)

    euc_dis = euclidean_distances(features, features)
    euc_dis = 1.0 - (euc_dis / np.max(euc_dis))

    similarity_matrix = np.zeros(cos_dis.shape)

    # averaging distances
    for i in range(similarity_matrix.shape[0]):
        for j in range(similarity_matrix.shape[1]):

            similarity_matrix[i,j] = (cos_dis[i, j] + rbf_ker[i, j] + 
                                      lap_ker[i, j] + euc_dis[i, j]) / 4.0
    return similarity_matrix


def get_similarity_score(id, mapping, similarity_matrix):
    try:
        index = mapping[id]
    except:
        print("ERROR: Wrong input city ID")
        return 1
    similarity_score = list(enumerate(similarity_matrix[index]))
    return similarity_score


def recsys_top_results(similarity_score, df, user_cities_list, user_seen_list):
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    #similarity_score = similarity_score[1:25]
    city_indeces = [i[0] for i in similarity_score]
    top_cities = [[x, y[1]] for x, y in zip(df['id'].iloc[city_indeces], similarity_score) if x not in user_cities_list and x not in user_seen_list]
    return top_cities


def update_scores(new_city, user_city_list,
                  prev_sim_scores,
                  cities_sim_matr,
                  cities_mapping):

    new_sim_scores = get_similarity_score(new_city, cities_mapping, cities_sim_matr)
    
    if new_sim_scores == 1:
        return 1, 1
    
    if len(user_city_list) != 0:
        scores = []
        for i in range(len(prev_sim_scores)):
            scores.append((i, new_sim_scores[i][1] + prev_sim_scores[i][1]))
        
        new_sim_scores=scores

    user_city_list.append(new_city)

    return user_city_list, new_sim_scores


def get_feature_grups():
    themes_dict = {}
    themes_dict['catering'] = {}
    themes_dict['catering']['color'] = '#d18f0b'
    themes_dict['catering']['title'] = 'Public Catering'
    themes_dict['catering']['xlabel'] = 'Cost, $'
    themes_dict['catering']['features'] = ['Cappuccino (regular)',
                                          'McMeal at McDonalds (or Equivalent Combo Meal)',
                                          'Meal, Inexpensive Restaurant',
                                          'Meal for 2 People, Mid-range Restaurant, Three-course']
    themes_dict['transport'] = {}
    themes_dict['transport']['color'] = '#6399d5'
    themes_dict['transport']['title'] = 'Transport'
    themes_dict['transport']['xlabel'] = 'Cost, $'
    themes_dict['transport']['features'] = ['Taxi 1 mile (Normal Tariff)',
                                            'One-way Ticket (Local Transport)',   
                                            'Taxi Start (Normal Tariff)', 
                                            'Gasoline (1 gallon)', 
                                            'Monthly Pass (Regular Price)']
    themes_dict['apartment'] = {}
    themes_dict['apartment']['color'] = '#a6244b'
    themes_dict['apartment']['title'] = 'Apartments'
    themes_dict['apartment']['xlabel'] = 'Cost, $'
    themes_dict['apartment']['features'] = ['Price per Square Feet to Buy Apartment Outside of Centre',
                                            'Price per Square Feet to Buy Apartment in City Centre',  
                                            'Apartment (1 bedroom) Outside of Centre', 
                                            'Apartment (3 bedrooms) Outside of Centre', 
                                            'Apartment (1 bedroom) in City Centre',
                                            'Apartment (3 bedrooms) in City Centre']
    themes_dict['edu/fin'] = {}
    themes_dict['edu/fin']['color'] = '#86bf91'
    themes_dict['edu/fin']['title'] = 'Education & Finance'
    themes_dict['edu/fin']['xlabel'] = 'Amount / Cost, $'
    themes_dict['edu/fin']['features'] = ['Average Monthly Net Salary (After Tax)',
                                          'Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child', 
                                          'International Primary School, Yearly for 1 Child']
    themes_dict['life-quality'] = {}
    themes_dict['life-quality']['color'] = '#a64d79'
    themes_dict['life-quality']['title'] = 'Quality of Life Factors'
    themes_dict['life-quality']['xlabel'] = 'Rate, %'
    themes_dict['life-quality']['features'] = ['Level of crime', 
                                              'Skill and competency of medical staff', 
                                              'Air Pollution', 
                                              'Drinking Water Pollution and Inaccessibility', 
                                              'Dissatisfaction with Green and Parks in the City']
    themes_dict['other'] = {}
    themes_dict['other']['color'] = '#bb9861'
    themes_dict['other']['title'] = 'Other Information'
    themes_dict['other']['xlabel'] = 'Cost, $'
    themes_dict['other']['features'] = ['Cigarettes 20 Pack (Marlboro)',  
                                        'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)',
                                        'Basic (Electricity, Heating, Cooling, Water, Garbage) for 915 sq ft Apartment',]            
    return themes_dict                                        


def visualize_theme(theme, city_id, themes_dict, data, path=None):
    # function to get barh matplotlib visualization of group of features.     #
    # theme - group of features (catering, transport, apartment, )            #
    # city_id - city to get info for, data - pd DataFrame with data,          #
    # path - path to a location where to store plot image                     #
    # (if path == None then just plot graph with no image saving)             #
    
    city_name, country_name = city_id.split('#')
    features = themes_dict[theme]['features']
    color = themes_dict[theme]['color']
    title = city_name + ', ' + country_name + ' - ' + themes_dict[theme]['title']
    xlabel = themes_dict[theme]['xlabel']

    sub_df = data[features][data['id']==city_id]
    
    fig, ax = plt.subplots(figsize=(10,5))

    y = ['\n'.join(wrap(x, 30)) for x in sub_df.columns]
    x = list(sub_df.values[0])

    ax.barh(y, x, color=color, zorder=2)

    for i, v in enumerate(x):
        ax.text(v + 3, i, str(v), va='center', 
                color=color, fontweight='bold', size=15)

    
    if theme == 'edu_fin':
        # create a list with two empty handles (or more if needed)
        handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", 
                                        lw=0, alpha=0)] * 2
        # create the corresponding number of labels (= the text you want to display)
        labels = []
        labels.append(str(data['Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate'][data['id']==city_id].values[0])+'%')
        labels.append('Mortgage Interest Rate Yearly,\nfor 20 Years Fixed-Rate')
        # create the legend, supressing the blank space of the empty line symbol and the
        # padding between symbol and label by setting handlelenght and handletextpad
        leg = ax.legend(handles, labels, loc='lower right', fontsize=14, 
                        fancybox=True, framealpha=0.7, 
                        handlelength=0, handletextpad=0, facecolor='#f3fff5')
        label1, label2 = leg.get_texts()
        label1._fontproperties = label2._fontproperties.copy()
        label1.set_size(25)
        label1.set_color(color)
        label1.set_weight('bold')

    
    if theme == 'life-quality':
        # create a list with two empty handles (or more if needed)
        handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", 
                                        lw=0, alpha=0)] * 2
        # create the corresponding number of labels (= the text you want to display)
        labels = []
        labels.append(str(data['Quality of Life Index:'][data['id']==city_id].values[0]))
        labels.append('Quality of Life Index\n(0..240)')
        # create the legend, supressing the blank space of the empty line symbol and the
        # padding between symbol and label by setting handlelenght and handletextpad
        leg = ax.legend(handles, labels, loc='lower right', fontsize=14, 
                        fancybox=True, framealpha=0.7, 
                        handlelength=0, handletextpad=0, facecolor='#ffe9f4')
        label1, label2 = leg.get_texts()
        label1._fontproperties = label2._fontproperties.copy()
        label1.set_size(25)
        label1.set_color(color)
        label1.set_weight('bold')

        labels = []
        labels.append(str(data['Traffic Index:'][data['id']==city_id].values[0]))
        labels.append('Traffic Index')
        leg2 = ax.legend(handles, labels, loc='upper right', fontsize=14, 
                         fancybox=True, framealpha=0.7, 
                         handlelength=0, handletextpad=0, facecolor='#ffe9f4')
        ax.add_artist(leg)

        label1, label2 = leg2.get_texts()
        label1._fontproperties = label2._fontproperties.copy()
        label1.set_size(25)
        label1.set_color(color)
        label1.set_weight('bold')
        plt.xlim([0, max(x) + 62])
    
    
    # Despine
    plt.box(False)
    # Switch off ticks
    plt.tick_params(axis=u'both', which=u'both', length=0, labelsize=15)
    # Draw vertical axis lines
    vals = ax.get_xticks()
    for tick in vals:
        ax.axvline(x=tick, linestyle='dashed', 
                   alpha=0.45, color='#cccccc', zorder=1)
    # Set x-axis label
    plt.xlabel(xlabel, labelpad=20, weight='bold', size=16)
    plt.title(title, weight='bold', size=16)
    # Format y-axis label
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))

    if path != None:    
        plt.savefig(path + city_id + '_' + theme + '_' + '.png', bbox_inches='tight')
        plt.close(fig)