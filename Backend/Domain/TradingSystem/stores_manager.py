from Backend.response import Response
from Backend.Domain.TradingSystem.Interfaces.IStore import IStore as store
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct as product


class StoresManager:
	stores : list[store] = []
	
	#2.5
	def get_stores_details() -> Response[list[store]]:
		return Response(True, StoresManager.stores)

	#2.5
	def get_products_by_store(store_id : str) -> Response[list[product]]:
		for store in StoresManager.stores:
			if store.get_id():
				return store.show_store_data()
		return Response(False, msg=f"Not store with the ID {store_id} exists")
	
	#2.6
	def get_products() -> list[product]:
		products_per_store = map(lambda store: store.show_store_data(), StoresManager.stores)
		products = []
		# iterating over the data
		for product_list in products_per_store:
			# appending elements to the flat_list
			products += product_list

		return products

	# Inter component functions
	#used in 3.2
	def create_store(store : store) -> None:
		StoresManager.stores.append(store)

	def get_store(store_id):
		for store in StoresManager.stores:
			if store.get_id():
				return Response(True, store)
		return Response(False, msg=f"Not store with the ID {store_id} exists")