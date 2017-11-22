<template>
<div id="ref-tables">
    <h2><b>Tra cứu</b></h2>

	<b-tabs>
		<b-tab title="Trường">
			<b-row>
				<b-col sm="5" offset-sm="7">
					<b-input-group>
						<b-input-group-addon><icon name="search"></icon></b-input-group-addon>
						<b-form-input type="text" placeholder="Tìm kiếm" v-model="schoolQuery"
							v-on:keyup.enter.native="search('searchedSchools', 'schoolQuery', 'http://localhost:5000/api/schools/search')">
						</b-form-input>
						<b-input-group-addon>
							<b-link href="#" v-on:click="resetSearch('searchedSchools', 'schoolQuery')">
								Hiện tất cả
							</b-link>
						</b-input-group-addon>
					</b-input-group>
				</b-col>
			</b-row>

			<div class="table-wrapper">
				<b-table striped hover :items="schoolDisp" :fields="schoolFields">
					<template slot="show_details" slot-scope="row">
						<b-form-checkbox v-model="row.item._showDetails"></b-form-checkbox>
					</template>
					<template slot="row-details" slot-scope="row">
						<b-card>
							<b-table :items="row.item.majors" :fields="schoolMajorFields"></b-table>
						</b-card>
					</template>
				</b-table>
			</div>
		</b-tab>

		<b-tab title="Ngành">
			<b-row>
				<b-col sm="5" offset-sm="7">
					<b-input-group>
						<b-input-group-addon><icon name="search"></icon></b-input-group-addon>
						<b-form-input type="text" placeholder="Tìm kiếm" v-model="majorQuery"
							v-on:keyup.enter.native="search('searchedMajors', 'majorQuery', 'http://localhost:5000/api/majors/search')">
						</b-form-input>
						<b-input-group-addon>
							<b-link href="#" v-on:click="resetSearch('searchedMajors', 'majorQuery')">
								Hiện tất cả
							</b-link>
						</b-input-group-addon>
					</b-input-group>
				</b-col>
			</b-row>

			<div class="table-wrapper">
				<b-table striped hover :items="majorDisp" :fields="majorFields">
					<template slot="show_details" slot-scope="row">
						<b-form-checkbox v-model="row.item._showDetails"></b-form-checkbox>
					</template>
					<template slot="row-details" slot-scope="row">
						<b-card>
							<b-table :items="row.item.schools" :fields="majorSchoolFields"></b-table>
						</b-card>
					</template>
				</b-table>
			</div>
		</b-tab>
	</b-tabs>
</div>
</template>

<script>
import 'vue-awesome/icons/search'
import $ from 'jquery'

export default {
	name: 'RefTables',
	data() {
		return {
			schools: null,
			schoolFields: {
				name: {label: 'Tên trường'},
				fee: {label: "Mức học phí"},
				ratio: {label: "Tỉ lệ chọi"},
				rank_score: {label: "Điểm xếp hạng"},
				show_details: {label: "Hiện danh sách ngành"}
			},
			schoolMajorFields: {
				name: {label: 'Ngành'},
				score_2015: {label: 'Điểm thi 2015'},
				score_2016: {label: 'Điểm thi 2016'},
				cutoff: {label: 'Chỉ tiêu'},
				group: {label: 'Khối'}
			},
			searchedSchools: null,
			schoolQuery: null,
			majors: null,
			majorFields: {
				name: {label: 'Tên ngành'},
				group: {label: 'Khối'},
				show_details: {label: "Hiện danh sách trường"}
			},
			majorSchoolFields: {
				name: {label: 'Trường'},
				ratio: {label: "Tỉ lệ chọi"},
				score_2015: {label: 'Điểm thi 2015'},
				score_2016: {label: 'Điểm thi 2016'},
				rank_score: {label: "Điểm xếp hạng"},
				cutoff: {label: 'Chỉ tiêu'}
			},
			searchedMajors: null,
			majorQuery: null
		}
	},
	computed: {
		schoolDisp() {
			if (this.searchedSchools) {
				return this.searchedSchools;
			} else if (this.schools) {
				return this.schools;
			} else return null;
		},
		majorDisp() {
			if (this.searchedMajors) {
				return this.searchedMajors;
			} else if (this.majors) {
				return this.majors;
			} else return null;
		}
	},
	methods: {
		resetSearch(key, queryKey) {
			this[key] = null;
			this[queryKey] = null;
		},
		search(key, queryKey, apiUrl) {
			if (!this[queryKey]) return;
			// console.log(apiUrl);
			var component = this;
			$.getJSON(apiUrl + '?query=' + this[queryKey], function(data){
				component[key] = data;
			});
		}
	},
	mounted() {
		var component = this;
		$.getJSON('http://localhost:5000/api/schools/all', function(data) {
			component.schools = data;
		})
		$.getJSON('http://localhost:5000/api/majors/all', function(data) {
			component.majors = data;
		})
	}
}
</script>

<style scoped>
#ref-tables {
	padding: 10px;
}

.table-wrapper {
	margin-top: 5px;
	max-height: 70vh;
	overflow-y: scroll;
	overflow-x: auto;
}
</style>
