from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from typing import Optional
import os

from azure.search.documents.indexes.models import (
    HnswParameters,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
    HnswParameters,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    VectorSearchAlgorithmMetric,
    SemanticConfiguration,  
    SemanticField,  
    SearchField, 
    SemanticPrioritizedFields,
    SemanticSearch,
    SearchableField
)

from azure.search.documents.models import (
    VectorQuery,
    VectorizedQuery,
    QueryType
)

AZURE_SEARCH_SERVICE=os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_ADMIN_KEY=os.getenv("AZURE_SEARCH_ADMIN_KEY")
AZURE_SEARCH_QUERY_KEY=os.getenv("AZURE_SEARCH_QUERY_KEY")


class AzureRetrieveApproach:
    def __init__(self):
        assert AZURE_SEARCH_SERVICE, "AZURE_SEARCH_SERVICE is not set"

        # self.__creds = DefaultAzureCredential()
        self.__creds = AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY)
        self.__index_client:  Optional[SearchIndexClient] = None
        self.__search_client:  Optional[SearchClient] = None

    def init_index_client(self):
        self.__index_client = SearchIndexClient(AZURE_SEARCH_SERVICE, credential=self.__creds)

    def init_search_client(self, index_name: str):
        self.__search_client = SearchClient(AZURE_SEARCH_SERVICE, index_name, credential=self.__creds)

    
    def create_index(self, indedx_name: str, embedding_dimension: int):
        fields = [  
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),  
            SimpleField(name="metadata", type=SearchFieldDataType.String, facetable=True),  
            SearchableField(name="title", type=SearchFieldDataType.String),  
            SearchableField(name="content", type=SearchFieldDataType.String),  
            SearchableField(name="category", type=SearchFieldDataType.String, filterable=True),  
            SearchField(
                name="titleVector", 
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),  
                searchable=True, 
                vector_search_dimensions=embedding_dimension, 
                vector_search_profile_name="myHnswProfile"
            ),  
            SearchField(
                name="contentVector", 
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),  
                searchable=True, 
                vector_search_dimensions=embedding_dimension, 
                vector_search_profile_name="myHnswProfile"
            ),  
        ]  
        
        # Configure the vector search configuration  
        vector_search = VectorSearch(  
            algorithms=[  
                HnswAlgorithmConfiguration(  
                    name="myHnsw",  
                    kind=VectorSearchAlgorithmKind.HNSW,  
                    parameters=HnswParameters(  
                        m=4,  
                        ef_construction=400,  
                        ef_search=500,  
                        metric=VectorSearchAlgorithmMetric.COSINE,  
                    )  
                ),  
            ],  
            profiles=[  
                VectorSearchProfile(  
                    name="myHnswProfile",  
                    algorithm_configuration_name="myHnsw",   
                ),  
            ],  
        )  
        
        semantic_config = SemanticConfiguration(  
            name="my-semantic-config",  
            prioritized_fields=SemanticPrioritizedFields(  
                title_field=SemanticField(field_name="title"),  
                keywords_fields=[SemanticField(field_name="category")],  
                content_fields=[SemanticField(field_name="content")]  
            )  
        )  
        
        # Create the semantic settings with the configuration  
        semantic_search = SemanticSearch(configurations=[semantic_config]) 
        
        
        index = SearchIndex(
            name=indedx_name, 
            fields=fields,
            vector_search=vector_search,
            semantic_search=semantic_search
        )

        self.init_index_client()

        result = self.__index_client.create_or_update_index(index)
        print(f'{result.name} created') 

    def update(self, documents: list[dict], index_name: str):
        if not self.__search_client:
            self.init_search_client(index_name=index_name)
        result = self.__search_client.upload_documents(documents=documents)
        # print(f'Indexed {len(result.results)} documents.')   

    def batch_update(self, documents: list[dict], index_name: str, batch_size: int = 1000):
        batch_documents = self.__make_batches(documents, batch_size=batch_size)
        for batch in batch_documents:
            self.update(batch, index_name=index_name)

    def __make_batches(self, input_list, batch_size=1000):
        result_list = []
        for i in range(0, len(input_list), batch_size):
            batch = input_list[i:i + batch_size]
            result_list.append(batch)
        return result_list
        
    def search(self, index_name: str, vector: list[float], fields:str , top: int = 10):
        self.init_search_client(index_name=index_name)

        vector_query = VectorizedQuery(
            vector=vector, 
            k_nearest_neighbors=5, 
            fields=fields
        )
        
        results = self.__search_client.search(  
            search_text=None,
            vector_queries= [vector_query], 
            select=["title", "metadata", "content", "category"],  
            top=top
        )  
        return results
    
    def hybrid_search(self, index_name: str, text: str, vector: list[float], fields:str , top: int = 10):
        self.init_search_client(index_name=index_name)

        vector_query = VectorizedQuery(
            vector=vector, 
            k_nearest_neighbors=top, 
            fields=fields
        )
        
        results = self.__search_client.search(  
            search_text=text,
            vector_queries= [vector_query], 
            select=["title", "metadata", "content", "category"],  
            top=top
        )  
        return results
    
    def hybrid_reranking_search(self, index_name: str, text: str, vector: list[float], fields:str , top: int = 10):
        self.init_search_client(index_name=index_name)

        vector_query = VectorizedQuery(
            vector=vector, 
            k_nearest_neighbors=top, 
            fields=fields
        )
        
        results = self.__search_client.search(  
            search_text=text,
            vector_queries= [vector_query], 
            select=["title", "metadata", "content", "category"],  
            top=top,
            query_type=QueryType.SEMANTIC, 
            semantic_configuration_name='my-semantic-config', 
            query_caption='extractive'
        )  
        return results