/
# coding: utf-8

'''
This script is used to get data on the composition of the dataset


'''

# In[1]:


import openslide
from os import listdir
from os.path import isfile


# ## AC class sample

# In[2]:


img_ac = openslide.OpenSlide("./ROI-dataset-bioinf/2_AC_1.svs")


# In[3]:


img_ac.dimensions


# In[5]:


img_ac.level_count


# In[30]:


img_ac_0=img_ac.read_region((0,0),0,(200,200))


# In[31]:


img_ac_0


# In[32]:


img_ac_1=img_ac.read_region((0,0),1,(200,200))


# In[33]:


img_ac_1


# In[35]:


img_ac_2=img_ac.read_region((0,0),2,(200,200))


# In[36]:


img_ac_2


# ## H class image sample

# In[13]:


img_h = openslide.OpenSlide("./ROI-dataset-bioinf/7_H_1.svs")


# In[14]:


img_h.level_count


# In[15]:


img_h.dimensions


# In[37]:


img_h_0=img_h.read_region((0,0),0,(200,200))


# In[38]:


img_h_0


# In[39]:


img_h_1=img_h.read_region((0,0),1,(200,200))


# In[40]:


img_h_1


# ## AD class image sample

# In[23]:


img_ad = openslide.OpenSlide("./ROI-dataset-bioinf/24_AD_1.svs")


# In[24]:


img_ad.level_count


# In[25]:


img_ad.dimensions


# In[41]:


img_ad_0 = img_ad.read_region((500,1000),0,(200,200))


# In[42]:


img_ad_0


# In[43]:


img_ad_1 = img_ad.read_region((500,500),1,(200,200))


# In[44]:


img_ad_1


# In[32]:





# ## In base alle immagini sopra, il livello di dettaglio migliore che è in grado di mostrare le informazioni necessarie in un immagine di 200px * 200px in tutti i tipi di tessuto è il livello 1.
